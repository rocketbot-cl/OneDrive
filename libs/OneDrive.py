import requests
import json
import os
import time
import uuid
from urllib.parse import parse_qs, quote, urlencode, urlparse


class OneDriveOAuthError(Exception):
    """OAuth error returned by Microsoft Entra ID."""

    REAUTHENTICATION_ERROR_CODES = {50173, 50089, 70000, 70008, 700082, 700084, 70043}

    def __init__(self, data, status_code=None):
        self.data = data if isinstance(data, dict) else {"error": "oauth_error", "error_description": str(data)}
        self.status_code = status_code
        message = self.data.get("error_description") or self.data.get("error") or "Microsoft OAuth authentication failed"
        super().__init__(message)

    @property
    def error_codes(self):
        codes = self.data.get("error_codes") or []
        normalized = set()
        for code in codes:
            try:
                normalized.add(int(code))
            except (TypeError, ValueError):
                continue
        return normalized

    @property
    def requires_reauthentication(self):
        return (
            self.data.get("error") in {"invalid_grant", "interaction_required", "consent_required", "login_required"}
            or bool(self.error_codes.intersection(self.REAUTHENTICATION_ERROR_CODES))
        )

    def as_dict(self):
        result = dict(self.data)
        if self.status_code is not None:
            result["status_code"] = self.status_code
        return result


class OneDriveReauthenticationRequired(OneDriveOAuthError):
    """Raised when delegated authentication needs a new interactive sign-in."""

    def __init__(self, data, authorization_url, status_code=None):
        super().__init__(data, status_code=status_code)
        self.authorization_url = authorization_url

    def as_dict(self):
        result = super().as_dict()
        result["reauthorization_required"] = True
        result["authorization_url"] = self.authorization_url
        return result


class OneDrive:
    def __init__(self, *, client_id, client_secret, tenant, redirect_uri=None,
                 path_credentials=None, auth_type="delegated", user_id=None, drive_id=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_type = self._normalize_auth_type(auth_type)
        self.scope = (
            "https://graph.microsoft.com/.default"
            if self.auth_type == "application"
            else "Files.ReadWrite.All offline_access"
        )
        self.redirect_uri = redirect_uri
        self.tenant = tenant
        self.access_token = None
        self.refresh_token = None
        self.path_credentials = path_credentials
        self.user_id = user_id
        self.drive_id = drive_id
        self.expires_at = 0
        self.request_timeout = 30

        if not self.client_id or not self.client_secret or not self.tenant:
            raise ValueError("client_id, client_secret and tenant are required")
        if self.auth_type == "delegated" and not self.redirect_uri:
            raise ValueError("redirect_uri is required for delegated authentication")
        if self.auth_type == "application" and not self.user_id and not self.drive_id:
            raise ValueError("user_id or drive_id is required for application authentication")

    @staticmethod
    def _normalize_auth_type(auth_type):
        value = str(auth_type or "delegated").strip().lower().replace("-", "_")
        if value in {"application", "app", "app_only", "client_credentials"}:
            return "application"
        if value in {"delegated", "authorization_code", "user"}:
            return "delegated"
        raise ValueError("auth_type must be 'delegated' or 'application'")

    def get_authorization_url(self, state=None):
        """Return the interactive authorization URL for delegated authentication."""
        if self.auth_type != "delegated":
            raise ValueError("Application authentication does not use an authorization URL")
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "response_mode": "query",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": state or uuid.uuid4().hex,
        }
        return "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?{query}".format(
            tenant=quote(str(self.tenant), safe=""),
            query=urlencode(params),
        )

    @staticmethod
    def extract_authorization_code(code_or_url):
        """Accept either a raw authorization code or the complete redirect URL."""
        value = str(code_or_url or "").strip()
        if not value:
            return None
        if "code=" not in value:
            return value
        parsed = urlparse(value)
        values = parse_qs(parsed.query).get("code")
        if not values and parsed.fragment:
            values = parse_qs(parsed.fragment).get("code")
        return values[0] if values else None

    def get_token(self, auth_code, grant_type):
        """ Get the access_token or refresh_token.

        The token that is obtained depends if it is the first time that the user is authenticated or not.

        Parameters
        ----------
        auth_code : dict
            Contains code or refresh_token
        grant_type : str
            Type of grant_type, it could be code or refresh_token

        Returns
        -------
        dict
            a json with the credentials
        """

        url, params = self.build_request(auth_code or {}, grant_type)
        try:
            response = requests.post(url, data=params, timeout=self.request_timeout)
        except requests.RequestException as exc:
            raise OneDriveOAuthError({
                "error": "token_request_failed",
                "error_description": str(exc),
            })

        try:
            json_response = response.json()
        except ValueError:
            raise OneDriveOAuthError({
                "error": "invalid_token_response",
                "error_description": response.text,
            }, status_code=response.status_code)

        if not response.ok or "error" in json_response or not json_response.get("access_token"):
            raise OneDriveOAuthError(json_response, status_code=response.status_code)

        self.access_token = json_response["access_token"]
        self.expires_at = time.time() + int(json_response.get("expires_in", 3600))
        new_refresh_token = json_response.get("refresh_token")
        if new_refresh_token:
            self.refresh_token = new_refresh_token
        elif self.auth_type == "delegated" and grant_type == "refresh_token" and self.refresh_token:
            json_response["refresh_token"] = self.refresh_token
        return json_response

    def build_request(self, auth_code, grant_type):
        """ Build the request.

        It depends if it is access_token or refresh_token.

        Parameters
        ----------
        auth_code : dict
            Contains code or refresh_token
        grant_type : str
            Type of grant_type, it could be code or refresh_token

        Returns
        -------
        string, dict
            a formed url and a dict with parameters

        """

        params = {
            "client_id": self.client_id,
            "scope": self.scope,
            "grant_type": grant_type,
            "client_secret": self.client_secret,
        }
        if self.auth_type == "delegated":
            params["redirect_uri"] = self.redirect_uri
        params.update(auth_code)
        url = 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'.format(tenant=self.tenant)
        return url, params

    def connect(self, code=None):
        """Authenticate using the configured mode and persist delegated tokens."""
        if self.auth_type == "application":
            return self.get_token({}, "client_credentials")

        stored_credentials = self.load_tokens_file()
        refresh_error = None
        if stored_credentials and stored_credentials.get("refresh_token"):
            self.refresh_token = stored_credentials["refresh_token"]
            try:
                response = self.get_token({"refresh_token": self.refresh_token}, "refresh_token")
                self.create_tokens_file(response)
                return response
            except OneDriveOAuthError as exc:
                if not exc.requires_reauthentication:
                    raise
                refresh_error = exc

        authorization_code = self.extract_authorization_code(code)
        if authorization_code:
            try:
                response = self.get_token({"code": authorization_code}, "authorization_code")
                self.create_tokens_file(response)
                return response
            except OneDriveOAuthError as exc:
                if not exc.requires_reauthentication:
                    raise
                refresh_error = refresh_error or exc

        error = refresh_error or OneDriveOAuthError({
            "error": "interaction_required",
            "error_description": "A fresh interactive authorization code is required.",
        })
        raise OneDriveReauthenticationRequired(
            error.as_dict(),
            authorization_url=self.get_authorization_url(),
            status_code=error.status_code,
        )

    def load_tokens_file(self):
        if not self.path_credentials:
            return None
        try:
            with open(self.path_credentials, "r", encoding="utf-8") as credential_file:
                data = json.load(credential_file)
            return data if isinstance(data, dict) else None
        except (OSError, ValueError, TypeError):
            return None

    def refresh_access_token(self):
        if self.auth_type == "application":
            return self.get_token({}, "client_credentials")
        if not self.refresh_token:
            stored_credentials = self.load_tokens_file() or {}
            self.refresh_token = stored_credentials.get("refresh_token")
        if not self.refresh_token:
            raise OneDriveReauthenticationRequired(
                {
                    "error": "interaction_required",
                    "error_description": "No delegated refresh token is available.",
                },
                authorization_url=self.get_authorization_url(),
            )
        try:
            response = self.get_token({"refresh_token": self.refresh_token}, "refresh_token")
        except OneDriveOAuthError as exc:
            if exc.requires_reauthentication:
                raise OneDriveReauthenticationRequired(
                    exc.as_dict(),
                    authorization_url=self.get_authorization_url(),
                    status_code=exc.status_code,
                )
            raise
        self.create_tokens_file(response)
        return response

    def ensure_access_token(self):
        if not self.access_token or time.time() >= self.expires_at - 300:
            self.refresh_access_token()

    def _request(self, method, url, **kwargs):
        """Call Microsoft Graph and refresh/retry once after an HTTP 401."""
        self.ensure_access_token()
        headers = dict(kwargs.pop("headers", {}) or {})
        headers["Authorization"] = "Bearer " + self.access_token
        timeout = kwargs.pop("timeout", self.request_timeout)
        response = requests.request(method, url, headers=headers, timeout=timeout, **kwargs)
        if response.status_code == 401:
            self.refresh_access_token()
            headers["Authorization"] = "Bearer " + self.access_token
            response = requests.request(method, url, headers=headers, timeout=timeout, **kwargs)
        return response

    def _drive_base_url(self, drive_id=None):
        selected_drive_id = drive_id or self.drive_id

        if selected_drive_id:
            selected_drive_id = str(selected_drive_id).strip()

            return "https://graph.microsoft.com/v1.0/drives/{drive_id}".format(
                drive_id=quote(selected_drive_id, safe="!@._-")
            )

        if self.auth_type == "application":
            user_id = str(self.user_id).strip()

            return "https://graph.microsoft.com/v1.0/users/{user_id}/drive".format(
                user_id=quote(user_id, safe="@._-")
            )

        return "https://graph.microsoft.com/v1.0/me/drive"

    def create_tokens_file(self, credentials):
        """ Create a json with credentials.

        Create a json with credentials.

        Parameters
        ----------
        credentials : dict
            Contains the credentials

        """

        try:
            if self.auth_type == "application":
                return True
            if not self.path_credentials:
                raise ValueError("path_credentials is required for delegated authentication")
            credentials_directory = os.path.dirname(self.path_credentials)
            if credentials_directory:
                os.makedirs(credentials_directory, exist_ok=True)
            temporary_path = self.path_credentials + ".tmp.{}".format(os.getpid())
            with open(temporary_path, "w", encoding="utf-8") as credfile:
                json.dump(credentials, credfile)
                credfile.flush()
                os.fsync(credfile.fileno())
            os.replace(temporary_path, self.path_credentials)
            return True
        except Exception as e:
            temporary_path = locals().get("temporary_path")
            if temporary_path and os.path.exists(temporary_path):
                try:
                    os.remove(temporary_path)
                except OSError:
                    pass
            print(e)
            raise e

    def get_items(self, order_by=None, filter_by=None, top=None):
        url = self._drive_base_url() + "/root/children"

        params = {}

        if order_by:
            params["$orderby"] = order_by
        if filter_by:
            params["$filter"] = filter_by
        if top:
            params["$top"] = top

        response = self._request("GET", url, params=params)

        try:
            json_response = response.json()
        except ValueError:
            json_response = {
                "error": {
                    "code": "invalidJsonResponse",
                    "message": response.text
                }
            }

        if not response.ok:
            error_result = {
                "error": json_response.get("error", json_response),
                "status_code": response.status_code,
                "request_url": response.request.url,
                "request_id": response.headers.get("request-id"),
                "client_request_id": response.headers.get("client-request-id"),
                "date": response.headers.get("Date"),
            }

            print(
                "[OneDrive Graph error] "
                + json.dumps(error_result, ensure_ascii=False)
            )

            return error_result

        return json_response
    
    def get_items_shared_with_me(self):
        """ List items shred to the current user's drive.

        Create a json with credentials.

        Returns
        -------
        dict
            shared items
        """
        if self.auth_type == "application":
            raise ValueError(
                "getItemsSharedWithMe is only available with delegated authentication. "
                "In application mode, use a known drive_id and listItems instead."
            )
        url = self._drive_base_url() + "/sharedWithMe"
        response = self._request("GET", url)
        json_response = json.loads(response.text)
        return json_response

    def list_items(self, item_id, drive_id=None, order_by=None, filter_by=None, top=None):
        result = []
        url = "{base}/items/{item_id}/children".format(
            base=self._drive_base_url(drive_id),
            item_id=quote(str(item_id), safe="!@._-"),
        )
            
        if order_by:
            url += "?$orderby={order_by}".format(order_by=order_by)
        if filter_by:
            url = url + "&" if order_by else url + "?"
            url += "$filter={filter}".format(filter=filter_by)
        if top:
            url = url + "&" if order_by or filter_by else url + "?"
            url += "$top={top}".format(top=top)
        
        response = self._request("GET", url)
        json_response = json.loads(response.text)
        result.append(json_response)
        while "@odata.nextLink" in json_response:
            response = self._request("GET", json_response["@odata.nextLink"])
            json_response = json.loads(response.text)
            result.append(json_response)
                        
        return result

    def get_info_items(self, item_id, drive_id=None):
        """Get details of a specific file or folder, whether shared or not.
        
        Parameters
        ----------
        item_id : str
            The ID of the item (file or folder).
        drive_id : str, optional
            The ID of the drive if the item is from a shared drive. Default is None.

        Returns
        -------
        dict
            Details of the file or folder
        """
        
        url = "{base}/items/{item_id}?$select=name,webUrl,size,lastModifiedDateTime,createdDateTime".format(
            base=self._drive_base_url(drive_id),
            item_id=quote(str(item_id), safe="!@._-"),
        )
        response = self._request("GET", url)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            return json_response
        else:
            return {'error': f"Failed to fetch item details. Status code: {response.status_code}, Response: {response.text}"}
    
    def download_item(self, item_id, folder_path, drive_id=None):
        url = "{base}/items/{item_id}".format(
            base=self._drive_base_url(drive_id),
            item_id=quote(str(item_id), safe="!@._-"),
        )
        response = self._request("GET", url)
        try:
            json_response = response.json()
        except Exception:
            return {'error': 'invalid_json', 'status_code': response.status_code, 'text': response.text}

        if 'error' in json_response:
            return json_response

        try:
            url_download = json_response.get('@microsoft.graph.downloadUrl')
            if not url_download:
                return {'error': 'no_download_url', 'response': json_response}

            filename = json_response.get('name') or item_id

            # downloadUrl is a pre-authenticated URL; do not send Authorization header
            response_download = requests.get(url_download, stream=True, timeout=self.request_timeout)

            if not response_download.ok:
                return {'error': 'download_failed', 'status_code': response_download.status_code, 'text': response_download.text}

            # ensure destination folder exists
            try:
                os.makedirs(folder_path, exist_ok=True)
            except Exception as e:
                return {'error': 'mkdir_failed', 'exception': str(e)}

            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'wb') as file:
                    for chunk in response_download.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
            except Exception as e:
                return {'error': 'write_failed', 'exception': str(e)}

            return True
        except Exception as e:
            return {'exception': str(e), 'response': json_response}

    def upload_item(self, file_path, drive_id, folder_path, conflict):
        headers = {'Content-Type': 'application/json'}
        # Before uploading it is necessary to open the file in binary for reading

        filename = file_path.split("/")[-1]
 
        total_file_size = os.path.getsize(file_path)
        if total_file_size > 4000000:
            
            body = {
                "item": {
                    "@microsoft.graph.conflictBehavior": conflict,
                    "name": filename
                }
            }
            upload_url = "{base}/items/{parent_id}:/{path}{filename}:/createUploadSession".format(
                base=self._drive_base_url(),
                parent_id=quote(str(drive_id), safe="!@._-"),
                path=folder_path,
                filename=filename,
            )
            upload_session = self._request("POST", upload_url, headers=headers, json=body).json()
            
            try:
                with open(file_path, 'rb') as f: 
                    chunk_size = 327680
                    chunk_number = total_file_size // chunk_size
                    chunk_leftover = total_file_size - chunk_size * chunk_number
                    i = 0
                    while True:
                        chunk_data = f.read(chunk_size)
                        start_index = i*chunk_size
                        end_index = start_index + chunk_size
                        #If end of file, break
                        if not chunk_data:
                            break
                        if i == chunk_number:
                            end_index = start_index + chunk_leftover
                        #Setting the header with the appropriate chunk data location in the file
                        headers_session = {
                            'Content-Length': f'{len(chunk_data)}',
                            'Content-Range': f'bytes {start_index}-{end_index-1}/{total_file_size}'
                            }
                        #Upload one chunk at a time
                        chunk_data_upload = requests.put(
                            upload_session['uploadUrl'],
                            data=chunk_data,
                            headers=headers_session,
                            timeout=self.request_timeout,
                        )
                        
                        if 'createdBy' in chunk_data_upload.json():
                            print("File upload compete")
                            return chunk_data_upload.json()
                        else:
                            print(f"File upload progress: {chunk_data_upload.json()}")
                        i = i + 1
                return chunk_data_upload.json()
            except KeyError:
                return upload_session
        else:
            with open(file_path, "rb") as file:
                fileHandle = file.read()
            
            resolution = f"?@microsoft.graph.conflictBehavior={conflict}"
            
            url = "{base}/items/{parent_id}:/{path}{filename}:/content{resolution}".format(
                base=self._drive_base_url(),
                parent_id=quote(str(drive_id), safe="!@._-"),
                path=folder_path,
                filename=filename,
                resolution=resolution,
            )
                
            response = self._request(
                "PUT",
                url,
                data=fileHandle,
                headers={'Content-Type': 'application/octet-stream'},
            )
            
            return response.json()
    
    def upload_item_shared_folder(self, file_path, drive_id, folder_id, conflict):
        headers = {'Content-Type': 'application/json'}
        # Before uploading it is necessary to open the file in binary for reading

        filename = file_path.split("/")[-1]
 
        total_file_size = os.path.getsize(file_path)
        if total_file_size > 4000000:
            
            body = {
                "item": {
                    "@microsoft.graph.conflictBehavior": conflict,
                    "name": filename
                }
            }
            
            upload_url = "{base}/items/{folder_id}:/{filename}:/createUploadSession".format(
                base=self._drive_base_url(drive_id),
                folder_id=quote(str(folder_id), safe="!@._-"),
                filename=filename,
            )
            upload_session = self._request("POST", upload_url, headers=headers, json=body).json()
           
            try:
                with open(file_path, 'rb') as f: 
                    chunk_size = 327680
                    chunk_number = total_file_size // chunk_size
                    chunk_leftover = total_file_size - chunk_size * chunk_number
                    i = 0
                    while True:
                        chunk_data = f.read(chunk_size)
                        start_index = i*chunk_size
                        end_index = start_index + chunk_size
                        #If end of file, break
                        if not chunk_data:
                            break
                        if i == chunk_number:
                            end_index = start_index + chunk_leftover
                        #Setting the header with the appropriate chunk data location in the file
                        headers_session = {
                            'Content-Length': f'{len(chunk_data)}',
                            'Content-Range': f'bytes {start_index}-{end_index-1}/{total_file_size}'
                            }
                        #Upload one chunk at a time
                        chunk_data_upload = requests.put(
                            upload_session['uploadUrl'],
                            data=chunk_data,
                            headers=headers_session,
                            timeout=self.request_timeout,
                        )
                        
                        if 'createdBy' in chunk_data_upload.json():
                            print("File upload compete")
                            return chunk_data_upload.json()
                        else:
                            print(f"File upload progress: {chunk_data_upload.json()}")
                        i = i + 1
                return chunk_data_upload.json()
            except KeyError:
                return upload_session
        else:
            with open(file_path, "rb") as file:
                fileHandle = file.read()
            
            resolution = f"?@microsoft.graph.conflictBehavior={conflict}"
            
            url = "{base}/items/{folder_id}:/{filename}:/content{resolution}".format(
                base=self._drive_base_url(drive_id),
                folder_id=quote(str(folder_id), safe="!@._-"),
                filename=filename,
                resolution=resolution,
            )
        
            response = self._request(
                "PUT",
                url,
                data=fileHandle,
                headers={'Content-Type': 'application/octet-stream'},
            )
            
            return response.json()
    
    def delete_item(self, item_id):
        """ Moves this item to the Recycle Bin

        :return: Success / Failure
        :rtype: bool
        """
        url = "{base}/items/{item_id}".format(
            base=self._drive_base_url(),
            item_id=quote(str(item_id), safe="!@._-"),
        )
        try:
            response = self._request("DELETE", url)
            
            if not response:
                return False

            return True
        except:
            return response
        
    def move_item(self, item_id, target_id):
        """ Moves this DriveItem to another Folder.
        Can't move between different Drives.

        :param target: a Folder, Drive item or Item Id string.
         If it's a drive the item will be moved to the root folder.
        :type target: drive.Folder or DriveItem or str
        :return: Success / Failure
        :rtype: bool
        """
        
        url = "{base}/items/{item_id}".format(
            base=self._drive_base_url(),
            item_id=quote(str(item_id), safe="!@._-"),
        )
        
        # if isinstance(target, Folder):
        #     target_id = target.object_id
        # elif isinstance(target, Drive):
        #     # we need the root folder id
        #     root_folder = target.get_root_folder()
        #     if not root_folder:
        #         return False
        #     target_id = root_folder.object_id
        # elif isinstance(target, str):
        #     target_id = target
        # else:
        #     raise ValueError('Target must be a Folder or Drive')

        # if not self.object_id or not target_id:
        #     raise ValueError(
        #         'Both self, and target must have a valid object_id.')

        if target_id == 'root':
            raise ValueError("When moving, target id can't be 'root'")

        # url = self.build_url(
        #     self._endpoints.get('item').format(id=self.object_id))

        try:
            payload = {"parentReference": {"id": "{target_id}".format(target_id=target_id)}}
            
            response = self._request("PATCH", url, json=payload)
            
            if not response:
                return False

            return True
        except:
            return response

    def copy_item(self, item_id, parent_id):
        """ Copies a DriveItem to another location within the same drive.
        
        :param item_id: ID of the item to be copied.
        :param parent_id: ID of the target folder.
        :return: Response JSON if the copy is successful
        """
        try:
            url = "{base}/items/{item_id}/copy".format(
                base=self._drive_base_url(),
                item_id=quote(str(item_id), safe="!@._-"),
            )
            
            payload = {"parentReference": {"id": "{parent_id}".format(parent_id=parent_id)}}
            
            response = self._request("POST", url, json=payload)
            
            if response.status_code == 202 or response.status_code == 200:
                return True
            else:
                print(response.json())
                return False
        except Exception as e:
            PrintException(e)
            return False

    def new_folder(self, item_id=None, name="NewFolder"):
            """Create new folder in OneDrive"""
            base = self._drive_base_url()
            if not item_id:
                url = base + "/root/children"
            else:
                url = "{base}/items/{item_id}/children".format(
                    base=base,
                    item_id=quote(str(item_id), safe="!@._-"),
                )

            try:
                payload = {"name": f"{name}", "folder": { }, "@microsoft.graph.conflictBehavior": "rename"}
                response = self._request("POST", url, json=payload)
                if not response:
                    return False
                return True
            except:
                print(f"Error: {response.status_code}, {response.text}")
                return response
            
    def new_folder_shared(self, drive_id, parent_item_id, name="NewFolder"):
        """Create new folder in a shared folder in OneDrive"""
        base = self._drive_base_url(drive_id)
        if not parent_item_id:
            url = base + "/root/children"
        else:
            url = "{base}/items/{parent_item_id}/children".format(
                base=base,
                parent_item_id=quote(str(parent_item_id), safe="!@._-"),
            )

        payload = {
            "name": name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }

        try:
            response = self._request("POST", url, json=payload)
            return response.json()
        except Exception as e:
            print(f"Error: {response.status_code}, {response.text}")
            return False
