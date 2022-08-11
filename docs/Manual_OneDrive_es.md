



# OneDrive
  
Working with OneDrive functions  
  
<!-- ![banner](/docs/imgs/Banner_C:\Users\jmsir\Desktop\RB\Rocketbot\modules\OneDrive.png) -->
## Como instalar este módulo
  
__Descarga__ e __instala__ el contenido en la carpeta 'modules' en la ruta de Rocketbot.  

## Como usar este modulo

Antes de usar este modulo, es necesario registrar tu aplicación en el portal de Azure App Registrations. 

1. Inicie sesión en Azure Portal (Registración de aplicaciones: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Seleccione "Nuevo registro".
3. En “Tipos de cuenta compatibles” soportados elija:
    a. "Cuentas en cualquier directorio organizativo (cualquier directorio de Azure AD: multiinquilino) y cuentas de Microsoft personales (como Skype o Xbox)" para este caso utilizar  ID Inquilino = common
    b. "Solo cuentas de este directorio organizativo (solo esta cuenta: inquilino único) para este caso utilizar ID Inquilino especifica de la aplicación.
4. Establezca la uri de redirección (Web) como: https://localhost/ y haga click en "Registrar".
5. Copie el ID de la aplicación (cliente). Necesitará este valor.
6. Dentro de "Certificados y secretos", genere un nuevo secreto de cliente. Establezca la caducidad (preferiblemente 24 meses). Copie el VALOR del secreto de cliente creado (NO el ID de Secreto). El mismo se ocultará al cabo de unos minutos.
7. Dentro de "Permisos de API", haga click en "Agregar un permiso", seleccione "Microsoft Graph", luego "Permisos delegados", busque y seleccione "Files.ReadWrite.All", y por ultimo "Agregar permisos".
8. Codigo de acceso, generar codigo ingresando al siguiente link:
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
Reemplazar dentro del link {tennat}, {client_id} y {redirect_uri}, por los datos correspondientes a la applicación creada.
9. Si la operación tuvo exito, la URL del navedador cambiara por: http://localhost:5000/?code={CODE}&state=12345#!/ 
El valor que figurara en {CODE}, copiarlo y utilizarlo en el comando de Rocketbot en el campo "code" para realizar la conexión.

Nota: El navegador NO cargara ninguna pagina.

## Descripción de los comandos

### Establecer credenciales
  
Establece las credenciales para tener disponible la API
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|client_id||Your client_id|
|client_secret||Your client_secret|
|redirect_uri||http://localhost:5000|
|code||code|
|tenant||tenant|
|Resultado|Variable para guardar resultado. Si la conexion es exitosa retornara True, caso contraria sera False|connection|

### Listar items de la raiz
  
Listar items de la raiz
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Resultado||res|

### Listar items de una carpeta
  
Listar items de una carpeta
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID de la carpeta||res|
|Resultado||res|

### Descargar archivo
  
Descarga un archivo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del archivo||id|
|Seleccionar una carpeta||Ruta a la carpeta|

### Subir archivo
  
Sube un archivo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID de la carpeta||res|
|Seleccionar un archivo||Ruta del archivo|
|Resultado|Variable para guardar resultado. Si la operacion es exitosa retornara True, caso contraria sera False|upload|
