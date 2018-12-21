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
    return


def token_time_to_live(client):
    '''
    以秒为单位获取令牌的到期时间。
    必须确保令牌可用。
    :param client:
    :return: OneDriveClient->int
    '''
    return int(client.auth_provider._session._expires_at - time())

def make_session_from_dict(status_dict):
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
        {'_expires_at': int(
          client.auth_provider._session._expires_at),
        'scope_string': ' '.join([str(i) for i in
                                 client.auth_provider._session.scope]),
        })


    status = json.dumps(status_dict)
    # 写入到对应的Json文件中
    with open(os.path.join(BASE_DIR,'driveJsons',fileName), "w+") as session_file:
        session_file.write(status)

def load_session(client,fileName):
    try:
        with open(os.path.join(BASE_DIR,'driveJsons',fileName), 'r') as session_file:
            status_dict = json.loads(session_file.read())
    except IOError as e:
        logging.fatal(e.strerror)
        logging.fatal('Cannot read the session file!')
        exit()

    if status_dict['is_business']:
        # mock http and auth
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(
            http_provider,
            client_id_business,
            auth_server_url=status_dict['client.auth_provider.auth_server_url'],
            auth_token_url=status_dict['client.auth_provider.auth_token_url'])

    else:
        # personal
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(
            http_provider=http_provider,
            client_id=status_dict['client_id'],
            scopes=scopes)

    ## Session 装填
    auth_provider._session = make_session_from_dict(status_dict)

    auth_provider.refresh_token()

    ## 推送 API endpoint
    return onedrivesdk.OneDriveClient(status_dict['client.base_url'], auth_provider, http_provider)