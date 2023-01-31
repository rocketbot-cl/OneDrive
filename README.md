# OneDrive
  
Work with OneDrive functions  

## How to install this module
  
__Download__ and __install__ the content in 'modules' folder in Rocketbot path  



## How to use this module

Before using this module, you need to register your app in the Azure App Registrations portal.

1. Sign in to the Azure portal (Applications Registration: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Select "New registration".
3. Under “Supported account types” supported choose:
    a. "Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)" for this case use Tenant ID = common
    b. "Accounts in this organizational directory only (This Account only - Single tenant)" for this case use application-specific Tenant ID.
4. Set the redirect uri (Web) as: https://localhost:5001/ and click "Register".
5. Copy the application (client) ID. You will need this value.
6. Under "Certificates and secrets", generate a new client secret. Set the expiration (preferably 24 months). Copy the VALUE of the created client secret (NOT the Secret ID). It will hide after a few minutes.
7. Under "API permissions", click "Add a permission", select "Microsoft Graph", then "Delegated permissions", find and select "Files.ReadWrite.All", and finally "Add permissions".
8. Access code, generate code by entering the following link:
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
Replace within the link {tennat}, {client_id} and {redirect_uri}, with the data corresponding to the created application.
9. If the operation was successful, the browser URL will change to: http://localhost:5001/?code={CODE}&state=12345#!/
The value that appears in {CODE}, copy it and use it in the Rocketbot command in the "code" field to make the connection.

Note: The browser will NOT load any pages.


## Overview


1. Set credentials  
Set credentials to make available the API

2. List root items  
List root items

3. List shared items  
List shared with me items

4. List items from a folder  
List items from a folder

5. Download item  
Download an item

6. Upload item  
Upload an item

7. Delete item  
Delete an item

8. Move item  
Move an item to another folder  




----
### OS

- windows
- mac
- linux

### Dependencies

### License
  
![MIT](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)  
[MIT](http://opensource.org/licenses/mit-license.ph)