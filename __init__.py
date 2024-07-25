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
if cur_path not in sys.path:
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
        SetVar(res, response)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

# Check that the connection has been stablished before executing any command
try:
    mod_OneDrive_session[session]
except:
    raise Exception("Must be connected before executing any command...")

if module == "getRootItems":
    order_by = GetParams("order_by") or None
    filter_by = GetParams("filter_by") or None
    top = GetParams("top") or None
    res = GetParams("res")
    try:
        response = mod_OneDrive_session[session].get_items(order_by, filter_by, top)
        try:
            values = response['value']
            folders = []
            for folder in values:
                dict_folder = {
                    'name': folder['name'],
                    'id': folder['id'],
                    'parent': folder['parentReference'],
                    'lastModifiedDateTime': folder['lastModifiedDateTime']
                }
                folders.append(dict_folder)
        except:
            folders = response
        SetVar(res, folders)
    except Exception as e:
        SetVar(res, response)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getItemsSharedWithMe":
    res = GetParams("res")
    try:
        response = mod_OneDrive_session[session].get_items_shared_with_me()
        try:
            values = response['value']
            folders = []
            for folder in values:
                dict_folder = {
                    'name': folder['name'],
                    'id': folder['id'],
                    'parent_drive_id': folder['remoteItem']['parentReference']['driveId'],
                    'lastModifiedDateTime': folder['lastModifiedDateTime']
                }
                folders.append(dict_folder)
        except:
            folders = response
        SetVar(res, folders)
    except Exception as e:
        SetVar(res, response)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "listItems":
    item_id = GetParams("item_id")
    drive_id = GetParams("drive_id")
    order_by = GetParams("order_by") or None
    filter_by = GetParams("filter_by") or None
    top = GetParams("top") or None
    res = GetParams("res")
    try:
        if drive_id and drive_id != "":
            response = mod_OneDrive_session[session].list_items(item_id, drive_id=drive_id, order_by=order_by, filter_by=filter_by, top=top)
        else:
            response = mod_OneDrive_session[session].list_items(item_id, order_by=order_by, filter_by=filter_by, top=top)
        try:
            items = []
            for r in response:
                values = r['value']
                for item in values:
                    dict_item = {
                        'name': item['name'],
                        'id': item['id'],
                        'lastModifiedDateTime': item['lastModifiedDateTime']
                    }
                    items.append(dict_item)
        except:
            items = response
        SetVar(res, items)
    except Exception as e:
        SetVar(res, response)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "downloadItem":
    item_id = GetParams("item_id")
    drive_id = GetParams("drive_id")
    folder = GetParams("folder")
    download = GetParams("download")
    
    if folder == "" or folder == None:
        raise Exception("Folder path needed!")
    try:
        if drive_id and drive_id != "":
            res = mod_OneDrive_session[session].download_item(item_id, folder, drive_id)
        else:
            res = mod_OneDrive_session[session].download_item(item_id, folder)
        SetVar(download, res)
    except Exception as e:
        SetVar(download, res)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "uploadItem":
    drive_id = GetParams("drive_id")
    path = GetParams("path")
    conflict = GetParams("conflict")
    filename = GetParams("filename")
    upload = GetParams("upload")
    res = GetParams("res")

    import traceback
    
    try:
        if drive_id == "" or drive_id == None:
            drive_id = "root"
        
        if path == "" or path == None:
            path = ""
        else:
            path = path + "/"
        
        if conflict == "" or conflict == None:
            conflict = "replace"
    
        res = mod_OneDrive_session[session].upload_item(filename, drive_id, path, conflict)
        SetVar(upload, res)
    except Exception as e:
        SetVar(upload, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
    
if module == "uploadItemSharedFolder":
    drive_id = GetParams("drive_id")
    folder_id = GetParams("folder_id")
    filename = GetParams("filename")
    conflict = GetParams("conflict")
    upload = GetParams("upload")
    
    if drive_id == "" or drive_id == None:
        raise Exception("Must give parent drive id of the shared folder...")
        
    if conflict == "" or conflict == None:
        conflict = "replace"
    
    try:
        res = mod_OneDrive_session[session].upload_item_shared_folder(filename, drive_id, folder_id, conflict)
        SetVar(upload, res)
    except Exception as e:
        SetVar(upload, res)
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
        SetVar(delete, res)
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
        SetVar(moved, res)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "newFolder":
    import traceback
    item_id = GetParams("item_id")
    name = GetParams("name")
    new = GetParams("new")
    
    try:
        res = mod_OneDrive_session[session].new_folder(item_id, name)
        SetVar(new, res)
    except Exception as e:
        traceback.print_exc()
        SetVar(new, res)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "newFolderSharedFolder":
    import traceback
    drive_id = GetParams("drive_id")
    item_id = GetParams("item_id")
    name = GetParams("name")
    new = GetParams("new")
    
    try:
        res = mod_OneDrive_session[session].new_folder_shared(drive_id, item_id, name)
        SetVar(new, res)
    except Exception as e:
        traceback.print_exc()
        SetVar(new, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
