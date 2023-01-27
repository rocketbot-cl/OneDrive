# OneDrive
  
Trabalhar com as funções do OneDrive  
  
![banner](imgs/Banner_OneDrive.png)
## Como instalar este módulo
  
__Baixe__ e __instale__ o conteúdo na pasta 'modules' no caminho do Rocketbot  





## Como usar este módulo

Antes de usar este módulo, você precisa registrar seu aplicativo no portal de Registros de Aplicativo do Azure.

1. Entre no portal do Azure (Registro de Aplicativos: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Selecione "Novo registro".
3. Em "Tipos de conta suportados", escolha:
    uma. "Contas em qualquer diretório organizacional (qualquer diretório do Azure AD - Multilocatário) e contas pessoais da Microsoft (por exemplo, Skype, Xbox)" para este caso, use ID do locatário = comum
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

## Descrição do comando

### Definir credenciais
  
Defina as credenciais para ter a API disponível
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|client_id||Your client_id|
|client_secret||Your client_secret|
|redirect_uri||http://localhost:5000|
|code||code|
|tenant||tenant|
|Resultado|Variável para armazenar resultado. Se a conexão for bem sucedida retornará True, caso contrário será False|connection|
|session||session|

### Listar itens raiz
  
Listar itens raiz
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Resultado||res|
|session||session|

### Listar itens partilhados
  
Listar os itens que foram partilhados comigo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Resultado||res|
|session||session|

### Listar itens em uma pasta
  
Listar itens em uma pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID da pasta||res|
|Resultado||res|
|session||session|

### Baixar arquivo
  
Baixar arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do arquivo||id|
|Selecione uma pasta||Caminho da pasta|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|download|
|session||session|

### Subir arquivo
  
Subir arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID Drive||root; 98CA2CA6789B976|
|Salvar caminho||Files/Reports|
|Resolução de conflitos||--- Select ---|
|Selecione um arquivo||Caminho de arquivo|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|upload|
|session||session|

### Excluir arquivo
  
Excluir um arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do arquivo||id|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|delete|
|session||session|

### Mover arquivo
  
Mover um arquivo para outra pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do arquivo||id|
|ID da pasta de destino||id|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|moved|
|session||session|
