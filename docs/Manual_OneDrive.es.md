



# OneDrive
  
Este módulo permite conectarse a la API de OneDrive, manejar archivos y carpetas alojados en la nube  

*Read this in other languages: [English](Manual_OneDrive.md), [Português](Manual_OneDrive.pr.md), [Español](Manual_OneDrive.es.md)*
  
![banner](imgs/Banner_OneDrive.png)
## Como instalar este módulo
  
Para instalar el módulo en Rocketbot Studio, se puede hacer de dos formas:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.  


## Como usar este modulo

Antes de usar este modulo, es necesario registrar tu aplicación en el portal de Azure App Registrations. 

1. Inicie sesión en Azure Portal (Registración de aplicaciones: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Seleccione "Nuevo registro".
3. En “Tipos de cuenta compatibles” soportados elija:
    - "Cuentas en cualquier directorio organizativo (cualquier directorio de Azure AD: multiinquilino) y cuentas de Microsoft personales (como Skype o Xbox)" para este caso utilizar  ID Inquilino = **common**.
    - "Solo cuentas de este directorio organizativo (solo esta cuenta: inquilino único) para este caso utilizar **ID Inquilino** especifico de la aplicación.
    - "Solo cuentas personales de Microsoft " for this case use use Tenant ID = **consumers**.
4. Establezca la uri de redirección (Web) como: https://localhost:5001/ y haga click en "Registrar".
5. Copie el ID de la aplicación (cliente). Necesitará este valor.

6. Dentro de "Certificados y secretos", genere un nuevo secreto de cliente. Establezca la caducidad (preferiblemente 24 meses). Copie el VALOR del secreto de cliente creado (NO el ID de Secreto). El mismo se ocultará al cabo de unos minutos.
7. Dentro de "Permisos de API", haga click en "Agregar un permiso", seleccione "Microsoft Graph", luego "Permisos delegados", busque y seleccione "Files.ReadWrite.All", y por ultimo "Agregar permisos".
8. Codigo de acceso, generar codigo ingresando al siguiente link:
https://login.microsoftonline.com/{**tenant**}/oauth2/v2.0/authorize?client_id={**client_id**}&response_type=code&redirect_uri={**redirect_uri**}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
Reemplazar dentro del link {tennat}, {client_id} y {redirect_uri}, por los datos correspondientes a la applicación creada.
9. Si la operación tuvo exito, la URL del navedador cambiara por: http://localhost:5001/?code={**CODE**}&state=12345#!/ 
El valor que figurara en 
{CODE}, copiarlo y utilizarlo en el comando de Rocketbot en el campo "code" para realizar la conexión.

Nota: El navegador NO cargara ninguna pagina.

## Descripción de los comandos

### Establecer credenciales
  
Establece las credenciales para tener disponible la API
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|client_id|ID de cliente obtenido en la creación de la aplicación|Your client_id|
|client_secret|Secreto del cliente obtenido en la creación de la aplicación|Your client_secret|
|redirect_uri|URL de redireccionamiento de la aplicación|http://localhost:5000|
|code|Dato obtenido al colocar la URL de autenticación. Revisa la documentación para más información|code|
|tenant|Identificador del tenant al que se desea conectar|tenant|
|Resultado|Variable para guardar resultado. Si la conexion es exitosa retornara True, caso contrario sera False|connection|
|session|Variable para guardar el identificador de sesión. Utilizar en caso de que desee conectarse a más de una cuenta de forma simultánea|session|

### Listar items de la raiz
  
Listar items de la raiz
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Resultado|Variable donde se guardará el resultado de la consulta|res|
|Ordenar por|Parámetros para ordenar los resultados de la consulta realizada|lastModifiedDateTime desc|
|Filter by|Filtro a aplicar para realizar la consulta|name eq 'file.txt'|
|Cantidad|Cantidad de items a obtener. Devolvera el top de items de la consulta.|10|
|session|Identificador de sesión|session|

### Listar items compartidos
  
Listar los items que me han compartido
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Resultado|Nombre de variable donde se guardará el resultado|res|
|session|Identificador de sesión|session|

### Listar items de una carpeta
  
Listar items de una carpeta
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID de la carpeta|ID de la carpeta que se desea listar|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|ID de Disco Compartido (Opcional)||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Ordenar por|Parámetros para ordenar los resultados de la consulta realizada|lastModifiedDateTime desc|
|Filter by|Filtro a aplicar para realizar la consulta|name eq 'file.txt'|
|Cantidad|Cantidad de items a obtener. Devolvera el top de items de la consulta.|10|
|Resultado|Nombre de la variable donde se guardará el resultado|res|
|session|Identificador de sesión|session|

### Descargar archivo
  
Descarga un archivo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del archivo|ID del archivo a descargar|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|ID de Disco Compartido (Opcional)||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Seleccionar una carpeta|Ruta a la carpeta donde se guardara el archivo|Ruta a la carpeta|
|Resultado|Variable para guardar resultado. Si la operacion es exitosa retornara True, caso contrario sera False|download|
|session|Identificador de sesión|session|

### Subir archivo
  
Sube un archivo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID Drive|ID del drive donde se subira el archivo.|root; 98CA2CA6789B976|
|Ruta de guardado|Ruta donde se guardara el archivo dentro del drive. Si no existe la ruta, la creará.|Files/Reports|
|Resolución de conflictos|Seleccionar que accion tomar ante un conflicto al subir un archivo. Por defecto se reemplaza el archivo.|--- Select ---|
|Seleccionar un archivo|Archivo que se desea subir al drive|Ruta del archivo|
|Resultado|Variable para guardar resultado. Si la operacion es exitosa retornara True, caso contrario sera False|upload|
|session|Identificador de sesión|session|

### Subir archivo a carpeta compartida
  
Sube un archivo a unacarpeta compartida
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID Drive||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Id de carpeta||15ZLM4OKQTAC3M7UDDR5DBUKPA4U8ULNXW|
|Seleccionar un archivo||Ruta del archivo|
|Resolución de conflictos||--- Select ---|
|Resultado|Variable para guardar resultado. Si la operacion es exitosa retornara True, caso contraria sera False|upload|
|session||session|

### Borrar archivo
  
Borrar un archivo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del archivo|ID del archivo que se desea borrar|id|
|Resultado|Variable para guardar resultado. Si la operacion es exitosa retornara True, caso contrario sera False|delete|
|session|Identificador de sesión|session|

### Mover archivo
  
Mover un archivo a otra carpeta
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del archivo|ID del archivo que se desea mover|id|
|ID de la carpeta de destino|ID de la carpeta donde se movera el archivo|id|
|Resultado|Variable para guardar resultado. Si la operacion es exitosa retornara True, caso contrario sera False|moved|
|session|Identificador de sesión|session|
