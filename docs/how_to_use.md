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
---
## Como usar este modulo

Antes de usar este modulo, es necesario registrar tu aplicación en el portal de Azure App Registrations. 

1. Inicie sesión en Azure Portal (Registración de aplicaciones: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Seleccione "Nuevo registro".
3. En “Tipos de cuenta compatibles” soportados elija:
    a. "Cuentas en cualquier directorio organizativo (cualquier directorio de Azure AD: multiinquilino) y cuentas de Microsoft personales (como Skype o Xbox)" para este caso utilizar  ID Inquilino = common
    b. "Solo cuentas de este directorio organizativo (solo esta cuenta: inquilino único) para este caso utilizar ID Inquilino especifica de la aplicación.
4. Establezca la uri de redirección (Web) como: https://localhost:5001/ y haga click en "Registrar".
5. Copie el ID de la aplicación (cliente). Necesitará este valor.
6. Dentro de "Certificados y secretos", genere un nuevo secreto de cliente. Establezca la caducidad (preferiblemente 24 meses). Copie el VALOR del secreto de cliente creado (NO el ID de Secreto). El mismo se ocultará al cabo de unos minutos.
7. Dentro de "Permisos de API", haga click en "Agregar un permiso", seleccione "Microsoft Graph", luego "Permisos delegados", busque y seleccione "Files.ReadWrite.All", y por ultimo "Agregar permisos".
8. Codigo de acceso, generar codigo ingresando al siguiente link:
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
Reemplazar dentro del link {tennat}, {client_id} y {redirect_uri}, por los datos correspondientes a la applicación creada.
9. Si la operación tuvo exito, la URL del navedador cambiara por: http://localhost:5001/?code={CODE}&state=12345#!/ 
El valor que figurara en {CODE}, copiarlo y utilizarlo en el comando de Rocketbot en el campo "code" para realizar la conexión.

Nota: El navegador NO cargara ninguna pagina.
---
## Como usar este módulo

Antes de usar este módulo, você precisa registrar seu aplicativo no portal de Registros de Aplicativo do Azure.

1. Entre no portal do Azure (Registro de Aplicativos: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Selecione "Novo registro".
3. Em "Tipos de conta suportados", escolha:
    a. "Contas em qualquer diretório organizacional (qualquer diretório do Azure AD - Multilocatário) e contas pessoais da Microsoft (por exemplo, Skype, Xbox)" para este caso, use ID do locatário = comum
    b. "Somente contas neste diretório organizacional (somente esta conta - locatário único)" para esse caso, use a ID de locatário específica do aplicativo.
4. Defina o redirecionamento uri (Web) como: https://localhost:5001/ e clique em "Registrar".
5. Copie o ID do aplicativo (cliente). Você vai precisar desse valor.
6. Em "Certificados e segredos", gere um novo segredo do cliente. Defina a validade (de preferência 24 meses). Copie o VALUE do segredo do cliente criado (NÃO o ID do segredo). Ele vai esconder depois de alguns minutos.
7. Em "Permissões de API", clique em "Adicionar uma permissão", selecione "Microsoft Graph", depois "Permissões delegadas", localize e selecione "Arquivos.ReadWrite.All" e, finalmente, "Adicionar permissões".
8. Acesse o código, gere o código entrando no seguinte link:
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
Substitua no link {tennat}, {client_id} e {redirect_uri}, pelos dados correspondentes ao aplicativo criado.
9. Se a operação for bem-sucedida, a URL do navegador será alterada para: http://localhost:5001/?code={CODE}&state=12345#!/
O valor que aparece em {CODE}, copie-o e use-o no comando Rocketbot no campo "code" para fazer a conexão.

Nota: O navegador NÃO carregará nenhuma página.