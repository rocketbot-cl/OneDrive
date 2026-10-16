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
| Allows listing “Shared with me” | Yes, with limitations | No |

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

5. Under **Redirect URI**, select the **Web** type and configure:

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

When this occurs, the command will return:

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

> Do not select “Delegated permissions”.

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
client_secret:   {Client Secret value}
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

In `Application` mode, the local credentials file is neither created nor read. The module requests a new `access_token` each time **Set credentials** is executed.

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

The `sharedWithMe` limitation does not prevent listing, downloading, uploading, or modifying a known item. It only prevents automatically retrieving the “Shared with me” collection.

For more information, see the [official Microsoft Graph documentation](https://learn.microsoft.com/en-us/graph/api/drive-sharedwithme?view=graph-rest-1.0).


#### Security considerations

- Do not share the Client Secret in screenshots, tickets, or log files. Use variables instead of the raw value in the connection command fields.
- Record the secret's expiration date and renew it before it expires.
- Execute **Set credentials** again after modifying permissions or renewing the secret.



---



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
| Requiere `user_id` o `target_drive_id` | No | Sí |
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
   - **Solo cuentas de este directorio organizativo:** utilizar el Tenant ID específico de la organización.
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

Para realizar la primera autenticación delegada, se debe obtener un código de autorización antes de ejecutar el comando **Establecer credenciales**.

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

6. Copiar únicamente el valor que aparece después de `code=` y antes de `&state`.

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

#### Reautenticación delegada

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

2. Abrir **Entra ID → Registros de aplicaciones**.

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

> Si la aplicación ya tiene un Client Secret vigente, podrá reutilizarse únicamente si la organización conserva su valor. El Id. del secreto no reemplaza al valor.

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

El comando **Listar items compartidos** utiliza el endpoint `sharedWithMe` de Microsoft Graph.

Este endpoint:

- Solo admite autenticación delegada.
- No funciona con permisos de tipo `Application`.
- Está obsoleto y Microsoft indica que dejará de devolver datos después de noviembre de 2026.

En modalidad `Application`, los elementos compartidos deben accederse directamente mediante un `drive_id` y un `item_id` conocidos.

La limitación de `sharedWithMe` no impide listar, descargar, cargar o modificar un elemento conocido. Únicamente impide obtener automáticamente la colección “Compartidos conmigo”.

Para más información, consultar la [documentación oficial de Microsoft Graph](https://learn.microsoft.com/en-us/graph/api/drive-sharedwithme?view=graph-rest-1.0).


#### Consideraciones de seguridad

- No compartir el Client Secret en capturas, tickets o archivos de log. Utilizar variables en vez del dato crudo en los campos del comando de conexión.
- Registrar la fecha de vencimiento del secreto y renovarlo antes de que expire.
- Ejecutar nuevamente **Establecer credenciales** después de modificar permisos o renovar el secreto.



---


## Como usar este módulo

Antes de utilizar o módulo, é necessário registrar um aplicativo no [Microsoft Entra](https://entra.microsoft.com/) e selecionar o método de autenticação que o processo utilizará.

O módulo oferece suporte a duas modalidades:

- **Delegated:** executa as operações em nome de um usuário.
- **Application (app-only):** autentica diretamente o aplicativo por meio de `client_credentials`, sem iniciar sessão com um usuário.

#### Comparação dos métodos de autenticação

| Característica | Delegated | Application |
|---|---|---|
| Identidade utilizada | Usuário autenticado | Aplicativo registrado |
| Permissão do Microsoft Graph | `Files.ReadWrite.All` - Delegated | `Files.ReadWrite.All` - Application |
| Requer código de autorização | Sim | Não |
| Requer URI de redirecionamento | Sim | Não |
| Utiliza arquivo local de credenciais | Sim | Não |
| Utiliza `refresh_token` | Sim | Não |
| Pode ser afetada por uma alteração de senha | Sim | Não |
| Requer `user_id` ou `target_drive_id` | Não | Sim |
| Permite listar “Compartilhados comigo” | Sim, com limitações | Não |

As permissões `Files.ReadWrite.All - Delegated` e `Files.ReadWrite.All - Application` podem coexistir no mesmo aplicativo. Adicionar a permissão de aplicativo não requer a remoção da permissão delegada existente.


### Autenticação delegada

A autenticação delegada executa as operações em nome de um usuário e mantém o funcionamento das versões anteriores do módulo.

#### Configuração no Microsoft Entra

1. Acesse o [Microsoft Entra](https://entra.microsoft.com/).

2. Abra **Entra ID → Registros de aplicativos**.

3. Selecione **Novo registro**.

4. Em **Tipos de conta com suporte**, selecione a opção correspondente:

   - **Contas em qualquer diretório organizacional e contas pessoais da Microsoft:** utilize `common` como Tenant ID.
   - **Somente contas deste diretório organizacional:** utilize o Tenant ID específico da organização.
   - **Somente contas pessoais da Microsoft:** utilize `consumers` como Tenant ID.

5. Em **URI de redirecionamento**, selecione o tipo **Web** e configure:

```text
https://localhost:5001/
```

6. Selecione **Registrar**.

7. Em **Visão geral**, copie o **ID do aplicativo (cliente)**.

8. Abra **Certificados e segredos → Segredos do cliente**.

9. Crie um novo segredo, defina a validade permitida pela organização e copie imediatamente o campo **Valor**.

> Deve-se utilizar o valor do Client Secret, não o ID do segredo.

10. Abra **Permissões de API → Adicionar uma permissão**.

11. Selecione **Microsoft Graph → Permissões delegadas**.

12. Pesquise e adicione:

```text
Files.ReadWrite.All
```

13. Conceda o consentimento necessário de acordo com as políticas da organização.

#### Primeira autenticação

Para realizar a primeira autenticação delegada, deve-se obter um código de autorização antes de executar o comando **Definir credenciais**.

1. Crie a seguinte URL:

```text
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
```

2. Substitua os seguintes valores:

   - `{tenant}`: Tenant ID configurado para o aplicativo, `common` ou `consumers`.
   - `{client_id}`: ID do aplicativo (cliente).
   - `{redirect_uri}`: URI de redirecionamento configurada no Microsoft Entra, por exemplo, `https://localhost:5001/`.

3. Abra a URL resultante no navegador.

4. Inicie sessão com o usuário que utilizará o OneDrive e aceite as permissões solicitadas.

5. Se a autenticação for bem-sucedida, o navegador redirecionará para uma URL semelhante a:

```text
https://localhost:5001/?code=<CODE>&state=12345
```

O navegador pode indicar que a página não está disponível. Isso é esperado; o código de autorização está dentro da URL.

6. Copie somente o valor que aparece depois de `code=` e antes de `&state`.

7. Configure o comando **Definir credenciais**:

```text
auth_type:       delegated
tenant:          {Tenant ID, common ou consumers}
client_id:       {Application/Client ID}
client_secret:   {valor do Client Secret}
redirect_uri:    https://localhost:5001/
code:            {código de autorização}
user_id:         vazio
target_drive_id: vazio
session:         {identificador da sessão}
```

8. Execute o comando.

Se a conexão for bem-sucedida, o resultado será:

```text
True
```

O módulo armazenará o `refresh_token` em:

```text
credentials.json
```

ou, se for utilizada uma sessão com nome:

```text
credentials_<session>.json
```

Nas execuções seguintes, o comando **Definir credenciais** deve ser mantido no início do processo. O módulo utilizará o arquivo existente para renovar o token automaticamente, portanto não será necessário gerar um novo código enquanto o `refresh_token` continuar válido.

#### Reautenticação delegada

A Microsoft pode revogar o `refresh_token` devido a uma alteração de senha, políticas de segurança ou expiração da sessão.

Quando isso ocorrer, o comando retornará:

```json
{
  "error": "invalid_grant",
  "error_description": "...",
  "reauthorization_required": true,
  "authorization_url": "https://login.microsoftonline.com/..."
}
```

Deve-se abrir a nova `authorization_url`, concluir o início de sessão e executar novamente **Definir credenciais** com o novo código ou com a URL completa de redirecionamento.


### Autenticação de aplicativo (app-only)

A autenticação `Application` não precisa iniciar sessão com um usuário nem utiliza `refresh_token`, portanto as alterações de senha não afetam a conexão.


#### Configuração no Microsoft Entra

Pode-se utilizar um aplicativo existente ou registrar um novo.

1. Acesse o [Microsoft Entra](https://entra.microsoft.com/) e selecione o tenant correto.

2. Abra **Entra ID → Registros de aplicativos**.

3. Selecione o aplicativo utilizado pelo processo.

4. Abra **Permissões de API → Adicionar uma permissão**.

5. Selecione **Microsoft Graph**.

6. Selecione **Permissões de aplicativo**.

> Não selecione “Permissões delegadas”.

7. Pesquise e adicione:

```text
Files.ReadWrite.All
```

8. Selecione **Conceder consentimento do administrador para a organização** e confirme.

9. Verifique se a permissão aparece da seguinte forma:

```text
API: Microsoft Graph
Permissão: Files.ReadWrite.All
Tipo: Application
Status: Concedido para <organização>
```

10. Em **Visão geral**, copie:

   - **ID do aplicativo (cliente):** será utilizado como `client_id`.
   - **ID do diretório (tenant):** será utilizado como `tenant`.

11. Abra **Certificados e segredos → Segredos do cliente**.

12. Crie um Client Secret e copie imediatamente o campo **Valor**.

> Se o aplicativo já tiver um Client Secret válido, ele poderá ser reutilizado somente se a organização conservar seu valor. O ID do segredo não substitui o valor.

#### Configuração por usuário

Para acessar o OneDrive de um usuário específico:

```text
auth_type:       application
tenant:          {Tenant ID no formato GUID}
client_id:       {Application/Client ID}
client_secret:   {valor do Client Secret}
user_id:         {UPN ou ID de objeto do usuário}
target_drive_id: vazio
redirect_uri:    vazio
code:            vazio
session:         {identificador da sessão}
```

O campo `user_id` pode conter:

- O UPN exato do usuário, por exemplo, `robot@empresa.com`.
- O ID de objeto do usuário obtido no Microsoft Entra.

O usuário deve pertencer ao tenant utilizado para obter o token e ter um OneDrive ativo.

#### Configuração por Drive ID

Se o identificador direto do OneDrive for conhecido:

```text
auth_type:       application
tenant:          {Tenant ID no formato GUID}
client_id:       {Application/Client ID}
client_secret:   {valor do Client Secret}
user_id:         vazio
target_drive_id: {Drive ID do OneDrive}
redirect_uri:    vazio
code:            vazio
session:         {identificador da sessão}
```

É obrigatório fornecer `user_id` ou `target_drive_id`.

Se ambos os campos forem preenchidos, `target_drive_id` terá prioridade sobre `user_id`.

Na modalidade `Application`, o arquivo local de credenciais não é criado nem consultado. O módulo solicita um novo `access_token` cada vez que **Definir credenciais** é executado.


#### Uso de sessões

O comando **Definir credenciais** deve ser executado uma vez no início do processo, antes de utilizar qualquer outro comando do OneDrive.

É possível utilizar autenticação delegada e de aplicativo no mesmo processo por meio de sessões diferentes:

```text
Delegated:   session = OneDriveDelegated
Application: session = OneDriveApplication
```

Se ambas as conexões utilizarem o mesmo nome de sessão, a segunda substituirá a primeira.


#### Itens compartilhados

O comando **Listar itens compartilhados** utiliza o endpoint `sharedWithMe` do Microsoft Graph.

Este endpoint:

- Oferece suporte apenas à autenticação delegada.
- Não funciona com permissões do tipo `Application`.
- Está obsoleto, e a Microsoft informa que deixará de retornar dados depois de novembro de 2026.

Na modalidade `Application`, os itens compartilhados devem ser acessados diretamente por meio de um `drive_id` e um `item_id` conhecidos.

A limitação de `sharedWithMe` não impede listar, baixar, carregar ou modificar um item conhecido. Ela apenas impede a obtenção automática da coleção “Compartilhados comigo”.

Para mais informações, consulte a [documentação oficial do Microsoft Graph](https://learn.microsoft.com/en-us/graph/api/drive-sharedwithme?view=graph-rest-1.0).


#### Considerações de segurança

- Não compartilhe o Client Secret em capturas de tela, tickets ou arquivos de log. Utilize variáveis em vez do dado bruto nos campos do comando de conexão.
- Registre a data de expiração do segredo e renove-o antes que expire.
- Execute novamente **Definir credenciais** depois de modificar as permissões ou renovar o segredo.