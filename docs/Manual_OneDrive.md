



# OneDrive
  
Working with OneDrive functions  
  
<!-- ![banner](/docs/imgs/Banner_C:\Users\jmsir\Desktop\RB\Rocketbot\modules\OneDrive.png) -->
## How to install this module
  
__Download__ and __install__ the content in 'modules' folder in Rocketbot path  



## Como usar este modulo

Antes de usar este modulo, es necesario registrar tu aplicación en el portal de Azure App 
Registrations. 

1. Inicie sesión en Azure Portal (Registración de aplicaciones: 
https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Seleccione "Nuevo registro".
3. 
En “Tipos de cuenta compatibles” soportados elija:
    a. "Cuentas en cualquier directorio organizativo (cualquier 
directorio de Azure AD: multiinquilino) y cuentas de Microsoft personales (como Skype o Xbox)" para este caso utilizar  
ID Inquilino = common
    b. "Solo cuentas de este directorio organizativo (solo esta cuenta: inquilino único) para este
 caso utilizar ID Inquilino especifica de la aplicación.
4. Establezca la uri de redirección (Web) como: 
https://localhost/ y haga click en "Registrar".
5. Copie el ID de la aplicación (cliente). Necesitará este valor.
6. 
Dentro de "Certificados y secretos", genere un nuevo secreto de cliente. Establezca la caducidad (preferiblemente 24 
meses). Copie el VALOR del secreto de cliente creado (NO el ID de Secreto). El mismo se ocultará al cabo de unos 
minutos.
7. Dentro de "Permisos de API", haga click en "Agregar un permiso", seleccione "Microsoft Graph", luego 
"Permisos delegados", busque y seleccione "Files.ReadWrite.All", y por ultimo "Agregar permisos".
8. Codigo de acceso, 
generar codigo ingresando al siguiente link:

https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345

Reemplazar dentro del link {tennat}, {client_id} y {redirect_uri}, por los datos correspondientes a la applicación 
creada.
9. Si la operación tuvo exito, la URL del navedador cambiara por: 
http://localhost:5000/?code={CODE}&state=12345#!/ 
El valor que figurara en {CODE}, copiarlo y utilizarlo en el comando 
de Rocketbot en el campo "code" para realizar la conexión.

Nota: El navegador NO cargara ninguna pagina.


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

### List root items
  
List root items
|Parameters|Description|example|
| --- | --- | --- |
|Result||res|

### List items from a folder
  
List items from a folder
|Parameters|Description|example|
| --- | --- | --- |
|Folder ID||res|
|Result||res|

### Download item
  
Download an item
|Parameters|Description|example|
| --- | --- | --- |
|File ID||id|
|Select a folder||Path to folder|

### Upload item
  
Upload an item
|Parameters|Description|example|
| --- | --- | --- |
|Folder ID||res|
|Select a file||Path file|
|Result|Variable to store result. If the task is successful, it will return True, otherwise it will return False|upload|
