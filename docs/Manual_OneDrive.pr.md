



# OneDrive
  
Este módulo permite que se conecte à API do OneDrive, gerencie arquivos e pastas hospedados na nuvem  

*Read this in other languages: [English](Manual_OneDrive.md), [Português](Manual_OneDrive.pr.md), [Español](Manual_OneDrive.es.md)*
  
![banner](imgs/Banner_OneDrive.png)
## Como instalar este módulo
  
Para instalar o módulo no Rocketbot Studio, pode ser feito de duas formas:
1. Manual: __Baixe__ o arquivo .zip e descompacte-o na pasta módulos. O nome da pasta deve ser o mesmo do módulo e dentro dela devem ter os seguintes arquivos e pastas: \__init__.py, package.json, docs, example e libs. Se você tiver o aplicativo aberto, atualize seu navegador para poder usar o novo módulo.
2. Automático: Ao entrar no Rocketbot Studio na margem direita você encontrará a seção **Addons**, selecione **Install Mods**, procure o módulo desejado e aperte instalar.  


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
| Requer `user_id` ou 
`target_drive_id` | Não | Sim |
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
   - **Somente contas pessoais da Microsoft:** 
utilize `consumers` como Tenant ID.

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

7. Configure o
 comando **Definir credenciais**:

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

A Microsoft pode revogar o `refresh_token` devido a uma alteração de 
senha, políticas de segurança ou expiração da sessão.

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

É obrigatório fornecer 
`user_id` ou `target_drive_id`.

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
- Não funciona com permissões do tipo 
`Application`.
- Está obsoleto, e a Microsoft informa que deixará de retornar dados depois de novembro de 2026.

Na modalidade `Application`, os itens compartilhados devem ser acessados diretamente por meio de um `drive_id` e um `item_id` conhecidos.

A limitação de `sharedWithMe` não impede listar, baixar, carregar ou modificar um item conhecido. Ela apenas impede a obtenção automática da coleção “Compartilhados comigo”.

Para mais informações, consulte a [documentação oficial do Microsoft Graph](https://learn.microsoft.com/en-us/graph/api/drive-sharedwithme?view=graph-rest-1.0).


#### Considerações de segurança

- Não compartilhe o Client Secret em capturas de tela, tickets ou arquivos de log. Utilize variáveis em vez do dado bruto nos campos do comando de conexão.
- Registre a data de expiração do segredo e renove-o antes que expire.
- Execute novamente **Definir credenciais** depois de modificar as permissões ou renovar o segredo.
## Descrição do comando

### Definir credenciais
  
Defina as credenciais para ter a API disponível
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Tipo de autenticação|Delegada mantém o comportamento anterior. Aplicação usa client credentials e não depende da senha do usuário.|--- Select ---|
|client_id|ID do cliente obtido na criação do aplicativo|Your client_id|
|client_secret|Segredo do cliente obtido na criação do aplicativo|Your client_secret|
|redirect_uri|Somente modo Delegado. Deve corresponder exatamente à URI configurada no Azure.|http://localhost:5001|
|code|Somente modo Delegado. Dados obtidos colocando a URL de autenticação. Verifique a documentação para mais informações|code|
|tenant|Identificador do tenant ao qual você deseja se conectar|tenant|
|Usuário de destino (user_id)|Somente modo Aplicação. UPN ou Object ID do usuário cujo OneDrive será usado. Não é necessário quando target_drive_id é informado.|robot@test.com or object ID|
|Drive de destino (target_drive_id)|Somente modo Aplicação. ID fixo do drive. Quando informado, tem prioridade sobre user_id.|OneDrive drive ID|
|Resultado|Variável para armazenar o resultado. Retorna True ou um objeto com detalhes OAuth e a URL de reautorização.|connection|
|session|Variável para armazenar o identificador da sessão. Use caso você queira se conectar a mais de uma conta ao mesmo tempo|session|

### Listar itens raiz
  
Listar itens raiz
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Resultado|Variável onde o resultado da consulta será salvo|res|
|Ordenar por|Parâmetros para ordenar os resultados da consulta realizada|lastModifiedDateTime desc|
|Filtrar por|Filtro a ser aplicado para realizar a consulta|name eq 'file.txt'|
|Quantia|Número de itens a serem obtidos. Ele retornará os principais itens da consulta|10|
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
|ID da pasta|ID da pasta a ser listada (pode ser um ID normal ou o 'remote_item_id' de uma pasta compartilhada)|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|ID do disco compartilhado (Opcional)|Utilize quando os arquivos a serem listados estiverem localizados em uma pasta compartilhada (este pode ser o 'remote_drive_id' de uma pasta compartilhada).|b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Ordenar por|Parâmetros para ordenar os resultados da consulta realizada|lastModifiedDateTime desc|
|Filtrar por|Filtro a ser aplicado para realizar a consulta|name eq 'file.txt'|
|Quantia|Número de itens a serem obtidos. Ele retornará os principais itens da consulta|10|
|Resultado|Nome da variável para salvar o resultado|res|
|session|ID da sessão|session|

### Obter dados de uma pasta ou arquivo
  
Listar itens em uma pasta ou arquivo, como o tamanho, a data de criação ou a data de modificação
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID da pasta ou arquivo|ID da pasta ou arquivo de onde os detalhes serão extraídos|23XWM5ASR67M67S6KYNCV66KFMQFOTOPDL|
|ID do disco compartilhado (Opcional)|Usar quando os arquivos ou pastas para serem listadas estão na pasta compartilhada.|b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
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

### Copiar arquivo
  
Copiar um arquivo para outra pasta
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do arquivo|ID do arquivo para mover|id|
|ID da pasta de destino|ID da pasta onde o arquivo será movido. Somente é possivel mover itens dentro do mesmo Drive|id|
|Resultado|Variável para armazenar resultado. Se a tarefa for bem sucedida, retornará True, caso contrário, retornará False|copied|
|session|ID da sessão|session|

### Criar pasta
  
Cria uma pasta em onde se indique
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID da pasta|ID da pasta onde a pasta será criada|id|
|Nome |Nome que receberá a pasta criada|id|
|Resultado|Variável para armazenar resultado.|new|
|session|ID da sessão|session|

### Criar pasta compartilhada
  
Cria uma pasta em uma pasta compartilhada
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID da pasta|É o remote_item_id obtido do comando Listar itens compartilhados|id|
|ID do disco compartilhado|É o parent_drive_id obtido do comando Listar itens compartilhados|b!4Zasr9LvqUiwt4OZ8irYdG3gm207yiJPkTu3c6KrXmFKVLpG3_FZTrGY-Gxn974J|
|Nome |Nome que receberá a pasta criada|id|
|Resultado|Variável para armazenar resultado.|new|
|session|ID da sessão|session|
