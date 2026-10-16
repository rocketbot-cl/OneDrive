



# OneDrive
  
Este módulo permite conectarse a la API de OneDrive, manejar archivos y carpetas alojados en la nube  

*Read this in other languages: [English](Manual_OneDrive.md), [Português](Manual_OneDrive.pr.md), [Español](Manual_OneDrive.es.md)*
  
![banner](imgs/Banner_OneDrive.png)

## Como instalar este módulo
  
Para instalar el módulo en Rocketbot Studio, se puede hacer de dos formas:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.  


## Cómo usar este módulo

Antes de utilizar el módulo, es necesario registrar una aplicación en [Microsoft Entra](https://entra.microsoft.com/) y seleccionar el método de autenticación que utilizará el proceso.

El módulo admite dos modalidades:

- **Delegated:** ejecuta las operaciones en representación de un usuario.
- **Application (app-only):** autentica directamente a la aplicación mediante `client_credentials`, sin iniciar sesión con un usuario.

#### Comparación de métodos de autenticación

| Característica | Delegated | Application |
|---|---|---|
| Identidad utilizada | Usuario autenticado | Aplicación registrada |
| Permiso de Microsoft Graph | `Files.ReadWrite.All` - Delegated | `Files.ReadWrite.All` - Application |
| Requiere código de autorización | Sí | No |
| Requiere URI de redirección | Sí | No |
| Utiliza archivo local de credenciales | Sí | No |
| Utiliza `refresh_token` | Sí | No |
| Puede verse afectada por un cambio de contraseña | Sí | No |
| Requiere `user_id` 
o `target_drive_id` | No | Sí |
| Permite listar “Compartidos conmigo” | Sí, con limitaciones | No |

Los permisos `Files.ReadWrite.All - Delegated` y `Files.ReadWrite.All - Application` pueden coexistir dentro de la misma aplicación. Agregar el permiso de aplicación no requiere eliminar el permiso delegado existente.


### Autenticación delegada

La autenticación delegada ejecuta las operaciones en representación de un usuario y mantiene el funcionamiento de las versiones anteriores del módulo.

#### Configuración en Microsoft Entra

1. Ingresar en [Microsoft Entra](https://entra.microsoft.com/).

2. Abrir **Entra ID → Registros de aplicaciones**.

3. Seleccionar **Nuevo registro**.

4. En **Tipos de cuenta admitidos**, seleccionar la opción correspondiente:

   - **Cuentas en cualquier directorio organizativo y cuentas personales de Microsoft:** utilizar `common` como Tenant ID.
   - **Solo cuentas de este directorio organizativo:** utilizar el Tenant ID específico de la 
organización.
   - **Solo cuentas personales de Microsoft:** utilizar `consumers` como Tenant ID.

5. En **URI de redirección**, seleccionar el tipo **Web** y configurar:

```text
https://localhost:5001/
```

6. Seleccionar **Registrar**.

7. En **Información general**, copiar el **Id. de aplicación (cliente)**.

8. Abrir **Certificados y secretos → Secretos de cliente**.

9. Crear un nuevo secreto, establecer la vigencia permitida por la organización y copiar inmediatamente el campo **Valor**.

> Se debe utilizar el valor del Client Secret, no el Id. del secreto.

10. Abrir **Permisos de API → Agregar un permiso**.

11. Seleccionar **Microsoft Graph → Permisos delegados**.

12. Buscar y agregar:

```text
Files.ReadWrite.All
```

13. Conceder el consentimiento requerido de acuerdo con las políticas de la organización.

#### Primera autenticación

Para realizar la primera autenticación delegada, se debe obtener un código de autorización antes de ejecutar el comando **Establecer 
credenciales**.

1. Construir la siguiente URL:

```text
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
```

2. Reemplazar los siguientes valores:

   - `{tenant}`: Tenant ID configurado para la aplicación, `common` o `consumers`.
   - `{client_id}`: Id. de aplicación (cliente).
   - `{redirect_uri}`: URI de redirección configurada en Microsoft Entra, por ejemplo `https://localhost:5001/`.

3. Abrir la URL resultante en el navegador.

4. Iniciar sesión con el usuario que utilizará OneDrive y aceptar los permisos solicitados.

5. Si la autenticación es exitosa, el navegador redirigirá a una URL similar a:

```text
https://localhost:5001/?code=<CODE>&state=12345
```

El navegador puede indicar que la página no está disponible. Esto es esperado; el código de autorización se encuentra dentro de la URL.

6. Copiar únicamente el 
valor que aparece después de `code=` y antes de `&state`.

7. Configurar el comando **Establecer credenciales**:

```text
auth_type:       delegated
tenant:          {Tenant ID, common o consumers}
client_id:       {Application/Client ID}
client_secret:   {valor del Client Secret}
redirect_uri:    https://localhost:5001/
code:            {código de autorización}
user_id:         vacío
target_drive_id: vacío
session:         {identificador de sesión}
```

8. Ejecutar el comando.

Si la conexión es exitosa, el resultado será:

```text
True
```

El módulo guardará el `refresh_token` en:

```text
credentials.json
```

o, si se utiliza una sesión con nombre:

```text
credentials_<session>.json
```

En las siguientes ejecuciones, se debe mantener el comando **Establecer credenciales** al inicio del proceso. El módulo utilizará el archivo existente para renovar el token automáticamente, por lo que no será necesario generar un código nuevo mientras el `refresh_token` continúe vigente.

#### 
Reautenticación delegada

Microsoft puede revocar el `refresh_token` debido a un cambio de contraseña, políticas de seguridad o expiración de la sesión.

Cuando esto ocurra, el comando devolverá:

```json
{
  "error": "invalid_grant",
  "error_description": "...",
  "reauthorization_required": true,
  "authorization_url": "https://login.microsoftonline.com/..."
}
```

Se debe abrir la nueva `authorization_url`, completar el inicio de sesión y volver a ejecutar **Establecer credenciales** con el nuevo código o con la URL completa de redirección.


### Autenticación de aplicación (app-only)

La autenticación `Application` no necesita iniciar sesión con un usuario ni utiliza `refresh_token`, por lo que los cambios de contraseña no afectan la conexión.


#### Configuración en Microsoft Entra

Puede utilizarse una aplicación existente o registrarse una nueva.

1. Ingresar en [Microsoft Entra](https://entra.microsoft.com/) y seleccionar el tenant correcto.

2. Abrir **Entra ID → Registros de
 aplicaciones**.

3. Seleccionar la aplicación utilizada por el proceso.

4. Abrir **Permisos de API → Agregar un permiso**.

5. Seleccionar **Microsoft Graph**.

6. Seleccionar **Permisos de aplicación**.

> No seleccionar “Permisos delegados”.

7. Buscar y agregar:

```text
Files.ReadWrite.All
```

8. Seleccionar **Conceder consentimiento de administrador para la organización** y confirmar.

9. Verificar que el permiso figure de la siguiente manera:

```text
API: Microsoft Graph
Permiso: Files.ReadWrite.All
Tipo: Application
Estado: Concedido para <organización>
```

10. En **Información general**, copiar:

   - **Id. de aplicación (cliente):** se utilizará como `client_id`.
   - **Id. de directorio (inquilino):** se utilizará como `tenant`.

11. Abrir **Certificados y secretos → Secretos de cliente**.

12. Crear un Client Secret y copiar inmediatamente el campo **Valor**.

> Si la aplicación ya tiene un Client Secret vigente, podrá reutilizarse únicamente si la organización conserva
 su valor. El Id. del secreto no reemplaza al valor.

#### Configuración mediante usuario

Para acceder al OneDrive de un usuario específico:

```text
auth_type:       application
tenant:          {Tenant ID en formato GUID}
client_id:       {Application/Client ID}
client_secret:   {valor del Client Secret}
user_id:         {UPN o Id. de objeto del usuario}
target_drive_id: vacío
redirect_uri:    vacío
code:            vacío
session:         {identificador de sesión}
```

El campo `user_id` puede contener:

- El UPN exacto del usuario, por ejemplo `robot@empresa.com`.
- El Id. de objeto del usuario obtenido desde Microsoft Entra.

El usuario debe pertenecer al tenant utilizado para obtener el token y disponer de un OneDrive activo.

#### Configuración mediante Drive ID

Si se conoce el identificador directo del OneDrive:

```text
auth_type:       application
tenant:          {Tenant ID en formato GUID}
client_id:       {Application/Client ID}
client_secret:   {valor del Client Secret}

user_id:         vacío
target_drive_id: {Drive ID del OneDrive}
redirect_uri:    vacío
code:            vacío
session:         {identificador de sesión}
```

Es obligatorio proporcionar `user_id` o `target_drive_id`.

Si se completan ambos campos, `target_drive_id` tiene prioridad sobre `user_id`.

En modalidad `Application` no se crea ni se consulta el archivo local de credenciales. El módulo solicita un nuevo `access_token` cada vez que se ejecuta **Establecer credenciales**.


#### Uso de sesiones

El comando **Establecer credenciales** debe ejecutarse una vez al inicio del proceso, antes de utilizar cualquier otro comando de OneDrive.

Es posible utilizar autenticación delegada y de aplicación dentro del mismo proceso mediante sesiones diferentes:

```text
Delegated:   session = OneDriveDelegated
Application: session = OneDriveApplication
```

Si ambas conexiones utilizan el mismo nombre de sesión, la segunda reemplazará a la primera.


#### Elementos compartidos

El comando 
**Listar items compartidos** utiliza el endpoint `sharedWithMe` de Microsoft Graph.

Este endpoint:

- Solo admite autenticación delegada.
- No funciona con permisos de tipo `Application`.
- Está obsoleto y Microsoft indica que dejará de devolver datos después de noviembre de 2026.

En modalidad `Application`, los elementos compartidos deben accederse directamente mediante un `drive_id` y un `item_id` conocidos.

La limitación de `sharedWithMe` no impide listar, descargar, cargar o modificar un elemento conocido. Únicamente impide obtener automáticamente la colección “Compartidos conmigo”.

Para más información, consultar la [documentación oficial de Microsoft Graph](https://learn.microsoft.com/en-us/graph/api/drive-sharedwithme?view=graph-rest-1.0).


#### Consideraciones de seguridad

- No compartir el Client Secret en capturas, tickets o archivos de log. Utilizar variables en vez del dato crudo en los campos del comando de conexión.
- Registrar la fecha de vencimiento del secreto y 
renovarlo antes de que expire.
- Ejecutar nuevamente **Establecer credenciales** después de modificar permisos o renovar el secreto.

## Descripción de los comandos

### Establecer credenciales
  
Establece las credenciales para tener disponible la API
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Tipo de autenticación|Delegada conserva el comportamiento anterior. Aplicación usa client credentials y no depende de la contraseña del usuario.|--- Select ---|
|client_id|ID de cliente obtenido en la creación de la aplicación|Your client_id|
|client_secret|Secreto del cliente obtenido en la creación de la aplicación|Your client_secret|
|redirect_uri|Solo modo Delegado. Debe coincidir exactamente con la URI configurada en Azure.|http://localhost:5001|
|code|Solo modo Delegado. Dato obtenido al colocar la URL de autenticación. Revisa la documentación para más información|code|
|tenant|Identificador del tenant al que se desea conectar|tenant|
|Usuario objetivo (user_id)|Solo modo Aplicación. UPN u Object ID del usuario cuyo OneDrive utilizará el robot. No es necesario si se informa target_drive_id.|robot@test.com or object ID|
|Drive objetivo (target_drive_id)|Solo modo Aplicación. ID fijo del drive. Si se completa, tiene prioridad sobre user_id.|OneDrive drive ID|
|Resultado|Variable para guardar el resultado. Devuelve True o un objeto con el detalle OAuth y la URL de reautorización.|connection|
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
|ID de la carpeta|ID de la carpeta que se desea listar,(puede ser un ID normal o el 'remote_item_id' de una carpeta compartida).|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|ID de Disco Compartido (Opcional)|Utilizar cuando los archivos a listar se encuentren en una carpeta compartida,(Puede ser el 'remote_drive_id'de una carpeta compartida.|b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Ordenar por|Parámetros para ordenar los resultados de la consulta realizada|lastModifiedDateTime desc|
|Filter by|Filtro a aplicar para realizar la consulta|name eq 'file.txt'|
|Cantidad|Cantidad de items a obtener. Devolvera el top de items de la consulta.|10|
|Resultado|Nombre de la variable donde se guardará el resultado|res|
|session|Identificador de sesión|session|

### Obtener datos de una carpeta o archivo
  
Lista información de una carpeta o archivo en específico, como el tamaño, la fecha de creación o la última modificación
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID de la carpeta o archivo|ID de la carpeta o archivo de la que se extraerán los detalles|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|ID de Disco Compartido (Opcional)|Utilizar cuando los archivos o carpetas se encuentran en una carpeta compartida.|b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
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

### Copiar archivo
  
Copia un archivo a otra carpeta
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del archivo|ID del archivo que se desea mover|id|
|ID de la carpeta de destino|ID de la carpeta donde se movera el archivo. Solo se puede mover elementos dentro del mismo Drive|id|
|Resultado|Variable para guardar resultado. Si la operacion es exitosa retornara True, caso contrario sera False|copied|
|session|Identificador de sesión|session|

### Crear carpeta
  
Crea una carpeta en donde se indique
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID de la carpeta|ID de la ubicación en que se desea crear la carpeta|id|
|Nombre |Nombre que recibirá la carpeta creada|id|
|Resultado|Variable para guardar resultado.|new|
|session|Identificador de sesión|session|

### Crear carpeta compartida
  
Crea una carpeta en una carpeta compartida
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID de la carpeta|Es el remote_item_id que se obtiene del comando Listar items compartidos |id|
|ID de Disco Compartido|Es el parent_drive_id que se obtiene del comando Listar items compartidos |b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Nombre |Nombre que recibirá la carpeta creada|id|
|Resultado|Variable para guardar resultado.|new|
|session|Identificador de sesión|session|
