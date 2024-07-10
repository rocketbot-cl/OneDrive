



# OneDrive
  
This module allows you to connect to the OneDrive API, handle files and folders hosted in the cloud  

*Read this in other languages: [English](Manual_OneDrive.md), [Português](Manual_OneDrive.pr.md), [Español](Manual_OneDrive.es.md)*
  
![banner](imgs/Banner_OneDrive.png)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  


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
|Folder ID|Folder ID to list|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|Shared Drive ID (Optional)||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Order by|Parameters to order the results of the query made|lastModifiedDateTime desc|
|Filtrar por|Filter to apply to perform the query|name eq 'file.txt'|
|Quantity|Number of items to obtain. It will return the top items of the query|10|
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

### Create Folder
  
Create a folder in where you want
|Parameters|Description|example|
| --- | --- | --- |
|Folder ID|Folder ID where the folder will be created|id|
|Name |Name that will receive the created folder|id|
|Result|Variable to store result.|new|
|session|Session ID|session|
