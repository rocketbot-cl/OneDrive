



# OneDrive
  
This module allows you to connect to the OneDrive API, handle files and folders hosted in the cloud  

*Read this in other languages: [English](Manual_OneDrive.md), [Português](Manual_OneDrive.pr.md), [Español](Manual_OneDrive.es.md)*
  
![banner](imgs/Banner_OneDrive.png)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  

## How to use this module

Before using this module, you need to register your app in the Azure App Registrations portal.

1. Sign in to the Azure portal (Applications Registration: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Select "New registration".
3. Under “Supported account types” supported choose:
    - "Accounts in any organizational directory (any Azure AD directory: multi-tenant) and personal Microsoft accounts (such as Skype or Xbox)" for this case use Tenant ID = **common**.
    - "Only accounts from this organizational directory (only this account: single tenant) for this case use application-specific **Tenant ID**.
    - "Personal Microsoft accounts only" for this case use use Tenant ID = **consumers**.
4. Set the redirect uri (Web) as: https://localhost:5001/ and click "Register".
5. Copy the application (client) ID. You will need this value.
6. Under "Certificates and secrets", generate a new client secret. Set the expiration 
(preferably 24 months). Copy the VALUE of the created client secret (NOT the Secret ID). It will hide after a few minutes.
7. Under "API permissions", click "Add a permission", select "Microsoft Graph", then "Delegated permissions", find and select "Files.ReadWrite.All", and finally "Add permissions".
8. Access code, generate code by entering the following link:
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={**client_id**}&response_type=code&redirect_uri={**redirect_uri**}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
Replace within the link {tennat}, {client_id} and {redirect_uri}, with the data corresponding to the created application.
9. If the operation was successful, the browser URL will change to: http://localhost:5001/?code={**CODE**}&state=12345#!/
The value that appears in {CODE}, copy it and use it in the Rocketbot command in the "code" field to make the connection.

Note: The browser will NOT load any pages.

## Description of the commands

### Set credentials
  
Set credentials to make available the API
|Parameters|Description|example|
| --- | --- | --- |
|client_id|Client ID obtained in the creation of the application|Your client_id|
|client_secret|Client secret obtained in the creation of the application|Your client_secret|
|redirect_uri|Application redirect URL|http://localhost:5000|
|code|Data obtained by placing the authentication URL. Check the documentation for more information|code|
|tenant|Tenant identifier to which you want to connect|tenant|
|Result|Variable to store result. If the connection is successful, it will return True, otherwise it will return False|connection|
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
