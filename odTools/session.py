import onedrivesdk
import logging
import json
from time import time
from alienVan.appConfig import *
from alienVan.settings import BASE_DIR  # 定位项目目录地址
from odTools.otherHandler import *

## Session maintain
## Session 维护


def get_access_token(client):
    '''
    获取将与所有请求一起使用的访问令牌，需要授权。
    这只是帮助自定义的辅助函数，下载和上传。
    :param client:
    :return: OneDriveClient->str
    '''
    return str(client.auth_provider.access_token)


def refresh_token(client):
    '''
    刷新客户端的token。
    一个令牌的默认过期时间为3600秒。
    :param client:
    :return: OneDriveClient->OneDriveClient
    '''
    client.auth_provider.refresh_token()
    return client


def token_time_to_live(client):
    '''
    以秒为单位获取令牌的到期时间。
    必须确保令牌可用。
    :param client:
    :return: OneDriveClient->int
    '''
    return int(client.auth_provider._session._expires_at - time())

def dict_to_Session(status_dict):
    return onedrivesdk.auth_provider.Session(
        status_dict['client.auth_provider._session']['token_type'],
        status_dict['client.auth_provider._session']['_expires_at'] - time(),
        status_dict['client.auth_provider._session']['scope_string'],
        status_dict['client.auth_provider._session']['access_token'],
        status_dict['client.auth_provider._session']['client_id'],
        status_dict['client.auth_provider._session']['auth_server_url'],
        status_dict['client.auth_provider._session']['redirect_uri'],
        refresh_token=status_dict['client.auth_provider._session']['refresh_token'],
        client_secret=status_dict['client.auth_provider._session']['client_secret'])


## Saving and Loading a Session
## Session 保存和读取


def save_session(client,fileName):
    if client.base_url == 'https://api.onedrive.com/v1.0/':
        # N
        status_dict = {
            'is_business': False,
            'client_id': client.auth_provider._client_id,
            'client.base_url': client.base_url,  # 'https://api.onedrive.com/v1.0/'
            'client.auth_provider.auth_token_url': client.auth_provider.auth_token_url, # 'https://login.live.com/oauth20_token.srf'
            'client.auth_provider.auth_server_url': client.auth_provider.auth_server_url,   # 'https://login.live.com/oauth20_authorize.srf'
            'client.auth_provider.scopes': client.auth_provider.scopes,
        }
        status_dict['client.auth_provider._session'] = dict_merge(
            client.auth_provider._session.__dict__,
            {'_expires_at': int(client.auth_provider._session._expires_at),
            'scope_string': ' '.join([str(i) for i in client.auth_provider._session.scope]),
            })
    else:
        # B
        status_dict = {
            'is_business': True,
            'client_id': client.auth_provider._client_id,
            'client.base_url': client.base_url,  #'https://{.....}.sharepoint.com/_api/v2.0/'
            'client.auth_provider.auth_token_url': client.auth_provider.auth_token_url,  #'https://login.microsoftonline.com/common/oauth2/token'
            'client.auth_provider.auth_server_url': client.auth_provider.auth_server_url[0],  #'https://login.microsoftonline.com/common/oauth2/authorize'
            'client.auth_provider.scopes': client.auth_provider.scopes,  # empty for business
        }

        status_dict['client.auth_provider._session'] = dict_merge(
            client.auth_provider._session.__dict__,
            {'_expires_at': int(client.auth_provider._session._expires_at),
            'scope_string': ' '.join([str(i) for i in client.auth_provider._session.scope]),
            })


    # 转成json对象并保存
    with open(os.path.join(BASE_DIR, 'driveJsons', fileName), "w+") as session_file:
        json.dump(status_dict, session_file)

    print(status_dict)
    print(type(status_dict))
    return status_dict

def load_session(status_dict):
    '''
    将传入的字典对象转为OD的client
    :param status_dict:
    :return: dict->OneDriveClient
    '''
    if status_dict['is_business']:
        # B
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(
            http_provider,
            client_id_business,
            auth_server_url=status_dict['client.auth_provider.auth_server_url'],
            auth_token_url=status_dict['client.auth_provider.auth_token_url'])

    else:
        # N
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(
            http_provider=http_provider,
            client_id=status_dict['client_id'],
            scopes=scopes)

    ## Session 装填
    auth_provider._session = dict_to_Session(status_dict)

    auth_provider.refresh_token()

    ## 推送 API endpoint
    return onedrivesdk.OneDriveClient(status_dict['client.base_url'], auth_provider, http_provider)


def navigate(client, item_id):
    # items = client.item(id=item_id).children.get()
    items = client.item(id=item_id).children.request(top=3).get()
    return items

if __name__ == '__main__':
    # 读取保存在json的session信息
    from odTools.otherHandler import json_file_to_dict
    temp = json_file_to_dict('/home/rq/workspace/python/AlienVan/driveJsons/233.json')
    client = load_session(temp)
    print(client)


    # 刷新session的 refresh_token
    client = refresh_token(client)
    save_session(client,'test2.json')


    # 列出项目的子项
    item_id = "root"    # 从根目录开始列出所有子项
    items = navigate(client, item_id)
    for i in items._prop_list:
        print(i)
    filesList = client.item(drive='me', id='root')
    print(filesList)
    print(type(filesList))


    # 上传
    # returned_item_up = client.item(drive='me', id='root').children['README.md'].upload('/home/rq/workspace/python/AlienVan/README.md')
    # returned_item_up = client.item(drive='me', id='root')
    # returned_item_up_ch = returned_item_up.children['README.md']
    # returned_item_up_ch_up = returned_item_up_ch.upload('/home/rq/workspace/python/AlienVan/README.md')


    # # 创建目录
    # f = onedrivesdk.Folder()
    # i = onedrivesdk.Item()
    # i.name = '测试文件夹'   # 新建的文件夹名
    # i.folder = f
    # returned_item_path = client.item(drive='me', id='root').children.add(i)


    # 重命名
    # renamed_item = onedrivesdk.Item()
    # renamed_item.name = 'NewItemName'
    # renamed_item.id = 'root'
    #
    # new_item = client.item(drive='me', id=renamed_item.id).update(renamed_item)