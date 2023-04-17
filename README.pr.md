# OneDrive
  
Este módulo permite que se conecte à API do OneDrive, gerencie arquivos e pastas hospedados na nuvem

*Read this in other languages: [English](README.md), [Português](README.pr.md), [Español](README.es.md)*

## Como instalar este módulo
  
__Baixe__ e __instale__ o conteúdo na pasta 'modules' no caminho do Rocketbot  

A instalação pode ser:
1. Manual: Baixe o arquivo .zip e descompacte-o na pasta de módulos. O nome da pasta deve ser o mesmo que o nome do módulo e dentro dele deve ter os seguintes arquivos e pastas: \__init__.py, package.json, docs, exemplo e libs. Se você tiver o aplicativo aberto, atualize o navegador para poder utilizar o novo módulo.
2. Automático: Ao entrar no Rocketbot Studio na margem direita, você encontrará a seção **Addons**, selecione **Install Mods**, encontre o módulo desejado e pressione instalar. 


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

## Overview


1. Definir credenciais  
Defina as credenciais para ter a API disponível

2. Listar itens raiz  
Listar itens raiz

3. Listar itens partilhados  
Listar os itens que foram partilhados comigo

4. Listar itens em uma pasta  
Listar itens em uma pasta

5. Baixar arquivo  
Baixar arquivo

6. Subir arquivo  
Subir arquivo

7. Excluir arquivo  
Excluir um arquivo

8. Mover arquivo  
Mover um arquivo para outra pasta  



### Changes
Tue Jan 31 09:34:33 2023  (HEAD -> qa, origin/qa) Merge pull request #7 from jmsiro/devJ
Fri Nov 11 14:05:38 2022  Merge pull request #5 from jmsiro/devJ
Tue Oct 4 17:08:45 2022  Merge pull request #4 from jmsiro/devJ
Thu Sep 1 20:12:08 2022  Merge pull request #3 from jmsiro/devJ
Wed Aug 24 17:51:16 2022  Merge pull request #1 from jmsiro/devJ

----
### OS

- windows
- mac
- linux

### Dependencies

### License
  
![MIT](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)  
[MIT](http://opensource.org/licenses/mit-license.ph)