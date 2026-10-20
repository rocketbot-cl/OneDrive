



# OneDrive
  
This module allows you to connect to the OneDrive API, handle files and folders hosted in the cloud  

*Read this in other languages: [English](Manual_OneDrive.md), [Português](Manual_OneDrive.pr.md), [Español](Manual_OneDrive.es.md)*
  
![banner](imgs/Banner_OneDrive.png)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  

## How to use this module

Before using the module, an application must be registered in [Microsoft Entra](https://entra.microsoft.com/) and the authentication method that the process will use must be selected.

The module supports two modes:

- **Delegated:** performs operations on behalf of a user.
- **Application (app-only):** authenticates the application directly using `client_credentials`, without signing in with a user.

#### Authentication method comparison

| Feature | Delegated | Application |
|---|---|---|
| Identity used | Authenticated user | Registered application |
| Microsoft Graph permission | `Files.ReadWrite.All` - Delegated | `Files.ReadWrite.All` - Application |
| Requires authorization code | Yes | No |
| Requires redirect URI | Yes | No |
| Uses a local credentials file | Yes | No |
| Uses `refresh_token` | Yes | No |
| May be affected by a password change | Yes | No |
| Requires `user_id` or `target_drive_id` | No | Yes |
| Allows listing “Shared with me” | Yes,
 with limitations | No |

The `Files.ReadWrite.All - Delegated` and `Files.ReadWrite.All - Application` permissions can coexist within the same application. Adding the application permission does not require removing the existing delegated permission.


### Delegated authentication

Delegated authentication performs operations on behalf of a user and preserves the behavior of previous module versions.

#### Configuration in Microsoft Entra

1. Sign in to [Microsoft Entra](https://entra.microsoft.com/).

2. Open **Entra ID → App registrations**.

3. Select **New registration**.

4. Under **Supported account types**, select the appropriate option:

   - **Accounts in any organizational directory and personal Microsoft accounts:** use `common` as the Tenant ID.
   - **Accounts in this organizational directory only:** use the organization's specific Tenant ID.
   - **Personal Microsoft accounts only:** use `consumers` as the Tenant ID.

5. Under **Redirect URI**, select the **Web** type 
and configure:

```text
https://localhost:5001/
```

6. Select **Register**.

7. Under **Overview**, copy the **Application (client) ID**.

8. Open **Certificates & secrets → Client secrets**.

9. Create a new secret, set the validity period permitted by the organization, and immediately copy the **Value** field.

> The Client Secret value must be used, not the Secret ID.

10. Open **API permissions → Add a permission**.

11. Select **Microsoft Graph → Delegated permissions**.

12. Search for and add:

```text
Files.ReadWrite.All
```

13. Grant the required consent according to the organization's policies.

#### First authentication

To perform the first delegated authentication, an authorization code must be obtained before executing the **Set credentials** command.

1. Build the following URL:

```text

https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
```

2. Replace the following values:

   - `{tenant}`: Tenant ID configured for the application, `common`, or `consumers`.
   - `{client_id}`: Application (client) ID.
   - `{redirect_uri}`: Redirect URI configured in Microsoft Entra, for example `https://localhost:5001/`.

3. Open the resulting URL in the browser.

4. Sign in with the user who will use OneDrive and accept the requested permissions.

5. If authentication is successful, the browser will redirect to a URL similar to:

```text
https://localhost:5001/?code=<CODE>&state=12345
```

The browser may indicate that the page is unavailable. This is expected; the authorization code is contained in the URL.

6. Copy only the value that appears after `code=` and before `&state`.

7. Configure the **Set credentials** command:


```text
auth_type:       delegated
tenant:          {Tenant ID, common, or consumers}
client_id:       {Application/Client ID}
client_secret:   {Client Secret value}
redirect_uri:    https://localhost:5001/
code:            {authorization code}
user_id:         empty
target_drive_id: empty
session:         {session identifier}
```

8. Execute the command.

If the connection is successful, the result will be:

```text
True
```

The module will store the `refresh_token` in:

```text
credentials.json
```

or, if a named session is used:

```text
credentials_<session>.json
```

On subsequent executions, the **Set credentials** command must remain at the beginning of the process. The module will use the existing file to renew the token automatically, so a new code will not need to be generated while the `refresh_token` remains valid.

#### Delegated reauthentication

Microsoft may revoke the `refresh_token` due to a password change, security policies, or session expiration.

When this 
occurs, the command will return:

```json
{
  "error": "invalid_grant",
  "error_description": "...",
  "reauthorization_required": true,
  "authorization_url": "https://login.microsoftonline.com/..."
}
```

The new `authorization_url` must be opened, sign-in completed, and **Set credentials** executed again with the new code or the complete redirect URL.


### Application authentication (app-only)

`Application` authentication does not require signing in with a user and does not use a `refresh_token`, so password changes do not affect the connection.


#### Configuration in Microsoft Entra

An existing application can be used, or a new one can be registered.

1. Sign in to [Microsoft Entra](https://entra.microsoft.com/) and select the correct tenant.

2. Open **Entra ID → App registrations**.

3. Select the application used by the process.

4. Open **API permissions → Add a permission**.

5. Select **Microsoft Graph**.

6. Select **Application permissions**.

> Do not select 
“Delegated permissions”.

7. Search for and add:

```text
Files.ReadWrite.All
```

8. Select **Grant admin consent for the organization** and confirm.

9. Verify that the permission appears as follows:

```text
API: Microsoft Graph
Permission: Files.ReadWrite.All
Type: Application
Status: Granted for <organization>
```

10. Under **Overview**, copy:

   - **Application (client) ID:** this will be used as `client_id`.
   - **Directory (tenant) ID:** this will be used as `tenant`.

11. Open **Certificates & secrets → Client secrets**.

12. Create a Client Secret and immediately copy the **Value** field.

> If the application already has a valid Client Secret, it can be reused only if the organization retains its value. The Secret ID does not replace the value.

#### Configuration using a user

To access a specific user's OneDrive:

```text
auth_type:       application
tenant:          {Tenant ID in GUID format}
client_id:       {Application/Client ID}
client_secret:   {Client Secret 
value}
user_id:         {user UPN or Object ID}
target_drive_id: empty
redirect_uri:    empty
code:            empty
session:         {session identifier}
```

The `user_id` field can contain:

- The user's exact UPN, for example `robot@empresa.com`.
- The user's Object ID obtained from Microsoft Entra.

The user must belong to the tenant used to obtain the token and have an active OneDrive.

#### Configuration using Drive ID

If the direct OneDrive identifier is known:

```text
auth_type:       application
tenant:          {Tenant ID in GUID format}
client_id:       {Application/Client ID}
client_secret:   {Client Secret value}
user_id:         empty
target_drive_id: {OneDrive Drive ID}
redirect_uri:    empty
code:            empty
session:         {session identifier}
```

It is mandatory to provide `user_id` or `target_drive_id`.

If both fields are completed, `target_drive_id` takes priority over `user_id`.

In `Application` mode, the local credentials file is neither created nor 
read. The module requests a new `access_token` each time **Set credentials** is executed.

#### Using sessions

The **Set credentials** command must be executed once at the beginning of the process, before using any other OneDrive command.

Delegated and application authentication can be used within the same process through different sessions:

```text
Delegated:   session = OneDriveDelegated
Application: session = OneDriveApplication
```

If both connections use the same session name, the second will replace the first.


#### Shared items

The **List shared items** command uses the Microsoft Graph `sharedWithMe` endpoint.

This endpoint:

- Only supports delegated authentication.
- Does not work with `Application` permissions.
- Is deprecated, and Microsoft indicates that it will stop returning data after November 2026.

In `Application` mode, shared items must be accessed directly using a known `drive_id` and `item_id`.

The `sharedWithMe` limitation does not prevent listing, 
downloading, uploading, or modifying a known item. It only prevents automatically retrieving the “Shared with me” collection.

For more information, see the [official Microsoft Graph documentation](https://learn.microsoft.com/en-us/graph/api/drive-sharedwithme?view=graph-rest-1.0).


#### Security considerations

- Do not share the Client Secret in screenshots, tickets, or log files. Use variables instead of the raw value in the connection command fields.
- Record the secret's expiration date and renew it before it expires.
- Execute **Set credentials** again after modifying permissions or renewing the secret.

## Description of the commands

### Set credentials
  
Set credentials to make available the API
|Parameters|Description|example|
| --- | --- | --- |
|Authentication type|Delegated keeps the previous behavior. Application uses client credentials and does not depend on the user's password.|--- Select ---|
|client_id|Client ID obtained in the creation of the application|Your client_id|
|client_secret|Client secret obtained in the creation of the application|Your client_secret|
|redirect_uri|Delegated mode only. It must exactly match the URI configured in Azure.|http://localhost:5001|
|code|Delegated mode only. Data obtained by placing the authentication URL. Check the documentation for more information|code|
|tenant|Tenant identifier to which you want to connect|tenant|
|Target user (user_id)|Application mode only. UPN or Object ID of the user whose OneDrive the robot will use. Not required when target_drive_id is provided.|robot@test.com or object ID|
|Target drive (target_drive_id)|Application mode only. Fixed drive ID. When provided, it takes precedence over user_id.|OneDrive drive ID|
|Result|Variable to store the result. Returns True or an object with OAuth details and the reauthorization URL.|connection|
|session|Variable to store the session identifier. Use in case you want to connect to more than one account at the same time|session|

### List root items
  
List root items
|Parameters|Description|example|
| --- | --- | --- |
|Result|Variable where the query result will be saved|res|
|Order by|Parameters to order the results of the query made|lastModifiedDateTime desc|
|Filtrar por|Filter to apply to perform the query|name eq 'file.txt'|
|Quantity|Number of items to obtain. It will return the top items of the query|10|
|session|Session ID|session|

### List shared items
  
List shared with me items
|Parameters|Description|example|
| --- | --- | --- |
|Result|Variable name where the result will be saved|res|
|session|Session ID|session|

### List items from a folder
  
List items from a folder
|Parameters|Description|example|
| --- | --- | --- |
|Folder ID|ID of the folder to be listed (this can be a normal ID or the 'remote_item_id' of a shared folder)|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|Shared Drive ID (Optional)|Use when the files to be listed are located in a shared folder (This can be the 'remote_drive_id' of a shared folder).|b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Order by|Parameters to order the results of the query made|lastModifiedDateTime desc|
|Filtrar por|Filter to apply to perform the query|name eq 'file.txt'|
|Quantity|Number of items to obtain. It will return the top items of the query|10|
|Result|Variable name to save the result|res|
|session|Session ID|session|

### Get data from a folder or file
  
List information from a folder or file, such as size, creation date or last modification
|Parameters|Description|example|
| --- | --- | --- |
|Folder or file ID|ID of the folder or file from which the details will be extracted|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|Shared Drive ID (Optional)|Use when the files or folders to be listed are in a shared folder.|b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Result|Variable name to save the result|res|
|session|Session ID|session|

### Download item
  
Download an item
|Parameters|Description|example|
| --- | --- | --- |
|File ID|File ID to download|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|Shared Drive ID (Optional)||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Select a folder|Path to folder where the file will be saved|Path to folder|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|download|
|session|Session ID|session|

### Upload item
  
Upload an item
|Parameters|Description|example|
| --- | --- | --- |
|Drive ID|ID of the drive where the file will be uploaded.|root; 98CA2CA6789B976|
|Save path|Route where the file will be saved within the drive. If the route doesn't exist, it will create.|Files/Reports|
|Conflict resolution|Select what action to take in case of a conflict when uploading a file. By default the file is replaced.|--- Select ---|
|Select a file|File to upload to the drive|Path file|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|upload|
|session|Session ID|session|

### Upload item to a shared folder
  
Upload an item to a shared folder
|Parameters|Description|example|
| --- | --- | --- |
|Drive ID||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Folder Id||15ZLM4OKQTAC3M7UDDR5DBUKPA4U8ULNXW|
|Select a file||Path file|
|Conflict resolution||--- Select ---|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|upload|
|session||session|

### Delete item
  
Delete an item
|Parameters|Description|example|
| --- | --- | --- |
|File ID|File ID to delete|id|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|delete|
|session|Session ID|session|

### Move item
  
Move an item to another folder
|Parameters|Description|example|
| --- | --- | --- |
|File ID|File ID to move|id|
|Target folder ID|Folder ID where the file will be moved|id|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|moved|
|session|Session ID|session|

### Copy item
  
Copy an item to another folder
|Parameters|Description|example|
| --- | --- | --- |
|File ID|File ID to move|id|
|Target folder ID|Folder ID where the file will be moved. You can only move items within the same Drive|id|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|copied|
|session|Session ID|session|

### Create Folder
  
Create a folder in where you want
|Parameters|Description|example|
| --- | --- | --- |
|Folder ID|Folder ID where the folder will be created|id|
|Name |Name that will receive the created folder|id|
|Result|Variable to store result.|new|
|session|Session ID|session|

### Create Shared Folder
  
Create a folder in a shared folder
|Parameters|Description|example|
| --- | --- | --- |
|Folder ID|Is the remote_item_id obtained from the List Shared Items command|id|
|Shared Drive ID|Is the parent_drive_id obtained from the List Shared Items command|b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Name |Name that will receive the created folder|id|
|Result|Variable to store result.|new|
|session|Session ID|session|
