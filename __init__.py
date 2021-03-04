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

global onedrive

if module == "setCredentials":
    client_secret = GetParams("client_secret")
    client_id = GetParams("client_id")
    redirect_uri = GetParams("redirect_uri")
    code = GetParams("code")
    tenant = GetParams("tenant")
    credentials_filename = 'credentials.json'
    path_credentials = base_path + "modules" + os.sep + "OneDrive" + os.sep + credentials_filename
    onedrive = OneDrive(client_id=client_id, client_secret=client_secret, tenant=tenant, redirect_uri=redirect_uri,
                        path_credentials=path_credentials)
    try:
        try:
            with open(path_credentials) as json_file:
                data = json.load(json_file)
            auth_code = {'refresh_token': data['refresh_token']}
            grant_type = 'refresh_token'
            response = onedrive.get_token(auth_code, grant_type)
        except IOError:
            grant_type = 'authorization_code'
            auth_code = {'code': code}
            response = onedrive.get_token(auth_code, grant_type)
        onedrive.create_tokens_file(response)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getRootItems":
    res = GetParams("res")
    try:
        values = onedrive.get_items()['value']
        folders = []
        for folder in values:
            dict_folder = {
                'name': folder['name'],
                'id': folder['id']
            }
            folders.append(dict_folder)
        print(folders)
        SetVar(res, folders)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "listItems":
    item_id = GetParams("item_id")
    res = GetParams("res")
    try:
        values = onedrive.list_items(item_id)['value']
        items = []
        for item in values:
            dict_item = {
                'name': item['name'],
                'id': item['id']
            }
            items.append(dict_item)
        print(items)
        SetVar(res, items)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "downloadItem":
    item_id = GetParams("item_id")
    folder = GetParams("folder")
    try:
        onedrive.download_item(item_id, folder)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "uploadItem":
    driver_id = GetParams("driver_id")
    filename = GetParams("filename")
    try:
        onedrive.upload_item(filename, driver_id)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e