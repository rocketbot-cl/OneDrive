# OneDrive
  
This module allows you to connect to the OneDrive API, handle files and folders hosted in the cloud

*Read this in other languages: [English](README.md), [Português](README.pr.md), [Español](README.es.md)*

## How to install this module
  
Installation can be:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The name of the folder must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh the browser to be able to use the new module.
2. Automatic: When you enter Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, find the desired module and press install.




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



### Changes
Tue Jan 31 09:34:33 2023  (HEAD -> qa, origin/qa) Merge pull request #7 from jmsiro/devJ
Fri Nov 11 14:05:38 2022  Merge pull request #5 from jmsiro/devJ
Tue Oct 4 17:08:45 2022  Merge pull request #4 from jmsiro/devJ
Thu Sep 1 20:12:08 2022  Merge pull request #3 from jmsiro/devJ
Wed Aug 24 17:51:16 2022  Merge pull request #1 from jmsiro/devJ

----
### OS

- windows
- mac
- linux

### Dependencies

### License
  
![MIT](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)  
[MIT](http://opensource.org/licenses/mit-license.ph)