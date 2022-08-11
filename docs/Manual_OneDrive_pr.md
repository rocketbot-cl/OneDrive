



# OneDrive
  
Working with OneDrive functions  
  
<!-- ![banner](/docs/imgs/Banner_C:\Users\jmsir\Desktop\RB\Rocketbot\modules\OneDrive.png) -->
## Como instalar este módulo
  
__Baixe__ e __instale__ o conteúdo na pasta 'modules' no caminho do Rocketbot  



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

### Listar itens raiz
  
Listar itens raiz
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Resultado||res|

### Listar itens em uma pasta
  
Listar itens em uma pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID da pasta||res|
|Resultado||res|

### Baixar arquivo
  
Baixar arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do arquivo||id|
|Selecione uma pasta||Caminho da pasta|

### Subir arquivo
  
Subir arquivo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID da pasta||res|
|Selecione um arquivo||Caminho de arquivo|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|upload|
