# OneDrive
  
Este módulo permite que se conecte à API do OneDrive, gerencie arquivos e pastas hospedados na nuvem  

  
*Read this in other languages: [English](Manual_OneDrive.md), [Português](Manual_OneDrive.pr.md), [Español](Manual_OneDrive.es.md)*  

  
![banner](imgs/Banner_OneDrive.png)
## Como instalar este módulo
  
Para instalar o módulo no Rocketbot Studio, pode ser feito de duas formas:
1. Manual: __Baixe__ o arquivo .zip e descompacte-o na pasta módulos. O nome da pasta deve ser o mesmo do módulo e dentro dela devem ter os seguintes arquivos e pastas: \__init__.py, package.json, docs, example e libs. Se você tiver o aplicativo aberto, atualize seu navegador para poder usar o novo módulo.
2. Automático: Ao entrar no Rocketbot Studio na margem direita você encontrará a seção **Addons**, selecione 
**Install Mods**, procure o módulo desejado e aperte instalar.  


## Como usar este módulo

Antes de usar este módulo, você precisa registrar seu aplicativo no portal de Registros de Aplicativo do Azure.

1. Entre no portal do Azure (Registro de Aplicativos: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Selecione "Novo registro".
3. Em "Tipos de conta suportados", escolha:
    uma. "Contas em qualquer diretório organizacional (qualquer diretório do Azure AD - Multilocatário) e contas pessoais da Microsoft (por 
exemplo, Skype, Xbox)" para este caso, use ID do locatário = comum
    b. "Somente contas neste diretório organizacional (somente esta conta - locatário único)" para esse caso, use a ID de locatário específica do aplicativo.
4. Defina o redirecionamento uri (Web) como: https://localhost:5001/ e clique em "Registrar".
5. Copie o ID do aplicativo (cliente). Você vai precisar desse valor.
6. Em "Certificados e segredos", gere um novo segredo do cliente. Defina a validade (de preferência 24 meses). 
Copie o VALUE do segredo do cliente criado (NÃO o ID do segredo). Ele vai esconder depois de alguns minutos.
7. Em "Permissões de API", clique em "Adicionar uma permissão", selecione "Microsoft Graph", depois "Permissões delegadas", localize e selecione "Arquivos.ReadWrite.All" e, finalmente, "Adicionar permissões".
8. Acesse o código, gere o código entrando no seguinte link:

https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=offline_access%20files.readwrite.all&state=12345
Substitua no link {tennat}, {client_id} e {redirect_uri}, pelos dados correspondentes ao aplicativo criado.
9. Se a operação for bem-sucedida, a URL do navegador será alterada para: http://localhost:5001/?code={CODE}&state=12345#!/
O valor que aparece em {CODE}, copie-o e use-o no comando 
Rocketbot no campo "code" para fazer a conexão.

Nota: O navegador NÃO carregará nenhuma página.
## Descrição do comando

### Definir credenciais
  
Defina as credenciais para ter a API disponível
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|client_id|ID do cliente obtido na criação do aplicativo|Your client_id|
|client_secret|Segredo do cliente obtido na criação do aplicativo|Your client_secret|
|redirect_uri|URL de redirecionamento do aplicativo|http://localhost:5000|
|code|Dados obtidos colocando a URL de autenticação. Verifique a documentação para mais informações|code|
|tenant|Identificador do tenant ao qual você deseja se conectar|tenant|
|Resultado|Variável para armazenar resultado. Se a conexão for bem sucedida retornará True, caso contrário será False|connection|
|session|Variável para armazenar o identificador da sessão. Use caso você queira se conectar a mais de uma conta ao mesmo tempo|session|

### Listar itens raiz
  
Listar itens raiz
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Resultado|Variável onde o resultado da consulta será salvo|res|
|session|ID da sessão|session|

### Listar itens partilhados
  
Listar os itens que foram partilhados comigo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Resultado|Nome da variável onde o resultado será guardado|res|
|session|ID da sessão|session|

### Listar itens em uma pasta
  
Listar itens em uma pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID da pasta|ID da pasta para listar|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|ID do disco compartilhado (Opcional)||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Resultado|Nome da variável para salvar o resultado|res|
|session|ID da sessão|session|

### Baixar arquivo
  
Baixar arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do arquivo|ID do arquivo para baixar|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|ID do disco compartilhado (Opcional)||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Selecione uma pasta|Caminho da pasta onde o arquivo será salvo|Caminho da pasta|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|download|
|session|ID da sessão|session|

### Subir arquivo
  
Subir arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID Drive|ID do drive onde o arquivo será carregado.|root; 98CA2CA6789B976|
|Salvar caminho|Rota onde o arquivo será salvo dentro do drive. Se a rota não existir, ela criará.|Files/Reports|
|Resolução de conflitos|Selecione qual ação tomar em caso de conflito ao carregar um arquivo. Por padrão, o arquivo é substituído.|--- Select ---|
|Selecione um arquivo|Arquivo para carregar no drive|Caminho de arquivo|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|upload|
|session|ID da sessão|session|

### Subir arquivo no drive compartilhado
  
Subir arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID Drive||b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Id do pasta||15ZLM4OKQTAC3M7UDDR5DBUKPA4U8ULNXW|
|Selecione um arquivo||Caminho de arquivo|
|Resolução de conflitos||--- Select ---|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|upload|
|session||session|

### Excluir arquivo
  
Excluir um arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do arquivo|ID do arquivo para excluir|id|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|delete|
|session|ID da sessão|session|

### Mover arquivo
  
Mover um arquivo para outra pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do arquivo|ID do arquivo para mover|id|
|ID da pasta de destino|ID da pasta onde o arquivo será movido|id|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|moved|
|session|ID da sessão|session|
