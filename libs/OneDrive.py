import requests
import json
import os


class OneDrive:
    def __init__(self, *, client_id, client_secret, tenant, redirect_uri, path_credentials):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = 'files.readwrite.all offline_access'
        self.redirect_uri = redirect_uri
        self.tenant = tenant
        self.access_token = None
        self.refresh_token = None
        self.path_credentials = path_credentials

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

        url, params = self.build_request(auth_code, grant_type)
        response = requests.post(url, data=params)
        json_response = json.loads(response.text)
        self.access_token = json_response['access_token']
        new_refresh_token = json_response['refresh_token']
        self.refresh_token = new_refresh_token
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
            'client_id': self.client_id,
            'scope': self.scope,
            'redirect_uri': self.redirect_uri,
            'grant_type': grant_type,
            'client_secret': self.client_secret,
        }
        params.update(auth_code)
        url = 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'.format(tenant=self.tenant)
        return url, params

    def create_tokens_file(self, credentials):
        """ Create a json with credentials.

        Create a json with credentials.

        Parameters
        ----------
        credentials : dict
            Contains the credentials

        """

        try:
            with open(self.path_credentials, 'w') as credfile:
                json.dump(credentials, credfile)
            return True
        except Exception as e:
            print(e)
            raise e

    def get_items(self):
        """ List children in the root of the current user's drive.

        Create a json with credentials.

        Returns
        -------
        dict
            folders in root
        """
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }
        url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
        response = requests.get(url, headers=headers)
        json_response = json.loads(response.text)
        return json_response

    def list_items(self, item_id):
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }
        url = "https://graph.microsoft.com/v1.0//me/drive/items/{item_id}/children".format(item_id=item_id)
        response = requests.get(url, headers=headers)
        json_response = json.loads(response.text)
        return json_response

    def download_item(self, item_id, folder_path):
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }
        url = "https://graph.microsoft.com/v1.0//me/drive/items/{item_id}/".format(item_id=item_id)
        response = requests.get(url, headers=headers)
        json_response = json.loads(response.text)
        url_download = json_response['@microsoft.graph.downloadUrl']
        filename = json_response['name']
        response_download = requests.get(url_download, headers=headers)
        # print(response_download.json())
        with open(folder_path + os.sep + filename, 'wb') as file:
            file.write(response_download.content)

    def upload_item(self, file_path, drive_id, folder_path):
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        # Before uploading it is necessary to open the file in binary for reading
        with open(file_path, "rb") as file:
            fileHandle = file.read()
        filename = file_path.split("/")[-1]
        # print(filename)
        url = "https://graph.microsoft.com/v1.0/me/drive/items/{drive_id}:/{folder_path}/{filename}:/content".format(
            drive_id=drive_id, filename=filename, folder_path=folder_path)
        response = requests.put(url, data=fileHandle, headers=headers)
        # print(response.json())
