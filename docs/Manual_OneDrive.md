



# OneDrive
  
Working with OneDrive functions  
  
![banner](imgs/Banner_OneDrive.png)
## How to install this module
  
__Download__ and __install__ the content in 'modules' folder in Rocketbot path  

## How to use this module

Before using this module, you need to register your app in the Azure App Registrations portal.

1. Sign in to the Azure portal (Applications Registration: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Select "New registration".
3. Under “Supported account types” supported choose:
    a. "Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)" for this case use Tenant ID = common
    b. "Accounts in this organizational directory only (This Account only - Single tenant)" for this case use application-specific Tenant ID.
4. Set the redirect uri (Web) as: https://localhost/ and click "Register".
5. Copy the application (client) ID. You will need this value.
6. Under "Certificates and secrets", generate a new client secret. Set the expiration (preferably 24 months). Copy the VALUE of the created client secret (NOT the Secret ID). It will hide after a few minutes.
7. Under "API permissions", click "Add a permission", select "Microsoft Graph", then "Delegated permissions", find and select "Files.ReadWrite.All", and finally "Add permissions".
8. Access code, generate code by entering the following link:
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
Replace within the link {tennat}, {client_id} and {redirect_uri}, with the data corresponding to the created application.
9. If the operation was successful, the browser URL will change to: http://localhost:5000/?code={CODE}&state=12345#!/
The value that appears in {CODE}, copy it and use it in the Rocketbot command in the "code" field to make the connection.

Note: The browser will NOT load any pages.

## Description of the commands

### Set credentials
  
Set credentials to make available the API
|Parameters|Description|example|
| --- | --- | --- |
|client_id||Your client_id|
|client_secret||Your client_secret|
|redirect_uri||http://localhost:5000|
|code||code|
|tenant||tenant|
|Result|Variable to store result. If the connection is successful, it will return True, otherwise it will return False|connection|
|session||session|

### List root items
  
List root items
|Parameters|Description|example|
| --- | --- | --- |
|Result||res|
|session||session|

### List items from a folder
  
List items from a folder
|Parameters|Description|example|
| --- | --- | --- |
|Folder ID||res|
|Result||res|
|session||session|

### Download item
  
Download an item
|Parameters|Description|example|
| --- | --- | --- |
|File ID||id|
|Select a folder||Path to folder|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|download|
|session||session|

### Upload item
  
Upload an item
|Parameters|Description|example|
| --- | --- | --- |
|Drive ID||root; 98CA2CA6789B976|
|Save path||Files/Reports|
|Select a file||Path file|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|upload|
|session||session|