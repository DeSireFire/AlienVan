import onedrivesdk
import logging
import json
from time import time
from alienVan.appConfig import *

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


## Saving and Loading a Session
## Session 保存和读取


def save_session(client):
    pass

def load_session(client):
    pass