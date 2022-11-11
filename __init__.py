# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"

    pip install <package> -t .

"""
import os
import sys
import json

base_path = tmp_global_obj["basepath"]
cur_path = base_path + "modules" + os.sep + "OneDrive" + os.sep + "libs" + os.sep
sys.path.append(cur_path)
"""
    Obtengo el modulo que fue invocado
"""
from OneDrive import OneDrive

module = GetParams("module")

global mod_OneDrive_session
global onedrive

session = GetParams("session")
if not session:
    session = ''

try:
    if not mod_OneDrive_session : #type:ignore
        mod_OneDrive_session = {}
except NameError:
    mod_OneDrive_session = {}

if module == "setCredentials":
    client_secret = GetParams("client_secret")
    client_id = GetParams("client_id")
    redirect_uri = GetParams("redirect_uri")
    code = GetParams("code")
    tenant = GetParams("tenant")
    res = GetParams("res")
    
    if session == '':
        credentials_filename = "credentials.json"
    else:
        credentials_filename = "credentials_{s}.json".format(s=session)
    
    path_credentials = base_path + "modules" + os.sep + "OneDrive" + os.sep + credentials_filename
    
    mod_OneDrive_session[session] = OneDrive(client_id=client_id, client_secret=client_secret, tenant=tenant, redirect_uri=redirect_uri, 
                                             path_credentials=path_credentials)
    try:
        try:
            with open(path_credentials) as json_file:
                data = json.load(json_file)
            auth_code = {'refresh_token': data['refresh_token']}
            grant_type = 'refresh_token'
            response = mod_OneDrive_session[session].get_token(auth_code, grant_type)
        except IOError:
            grant_type = 'authorization_code'
            auth_code = {'code': code}
            response = mod_OneDrive_session[session].get_token(auth_code, grant_type)
        is_connected = mod_OneDrive_session[session].create_tokens_file(response)
        SetVar(res,is_connected)
    except Exception as e:
        SetVar(res, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

# Check that the connection has been stablished before executing any command
try:
    mod_OneDrive_session[session]
except:
    raise Exception("Must be connected before executing any command...")

if module == "getRootItems":
    res = GetParams("res")
    try:
        values = mod_OneDrive_session[session].get_items()['value']
        folders = []
        for folder in values:
            dict_folder = {
                'name': folder['name'],
                'id': folder['id'],
                'parent': folder['parentReference']
            }
            folders.append(dict_folder)
        SetVar(res, folders)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getItemsSharedWithMe":
    res = GetParams("res")
    try:
        values = mod_OneDrive_session[session].get_items_shared_with_me()['value']
        folders = []
        for folder in values:
            dict_folder = {
                'name': folder['name'],
                'id': folder['id'],
            }
            folders.append(dict_folder)
        SetVar(res, folders)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "listItems":
    item_id = GetParams("item_id")
    res = GetParams("res")
    try:
        values = mod_OneDrive_session[session].list_items(item_id)['value']
        items = []
        for item in values:
            dict_item = {
                'name': item['name'],
                'id': item['id']
            }
            items.append(dict_item)
        SetVar(res, items)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "downloadItem":
    item_id = GetParams("item_id")
    folder = GetParams("folder")
    download = GetParams("download")
    
    if folder == "" or folder == None:
        raise Exception("Folder path needed!")
    try:
        res = mod_OneDrive_session[session].download_item(item_id, folder)
        SetVar(download, res)
    except Exception as e:
        SetVar(download, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "uploadItem":
    driver_id = GetParams("driver_id")
    path = GetParams("path")
    filename = GetParams("filename")
    upload = GetParams("upload")
    
    if driver_id == "" or driver_id == None:
        driver_id = "root"
    
    try:
        res = mod_OneDrive_session[session].upload_item(filename, driver_id, path)
        SetVar(upload, res)
    except Exception as e:
        SetVar(upload, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "deleteItem":
    item_id = GetParams("item_id")
    delete = GetParams("delete")
        
    try:
        res = mod_OneDrive_session[session].delete_item(item_id)
        SetVar(delete, res)
    except Exception as e:
        SetVar(delete, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "moveItem":
    item_id = GetParams("item_id")
    target_id = GetParams("target_id")
    moved = GetParams("moved")
    
    if target_id == "" or target_id == None:
        raise Exception("The folder target ID is needed!")
    try:
        res = mod_OneDrive_session[session].move_item(item_id, target_id)
        SetVar(moved, res)
    except Exception as e:
        SetVar(moved, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e