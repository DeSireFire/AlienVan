import requests
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
    pass
    # return str(client.auth_provider.access_token)


def refresh_token(refresh_token):
    '''
    刷新客户端的token。
    一个令牌的默认过期时间为3600秒。
    :param client:
    :return: OneDriveClient->OneDriveClient
    :param refresh_token: 字符串，原旧的令牌
    :return:
    '''
    data = {
        'client_id':oauthDict['app_id'],
        'redirect_uri':oauthDict['redirect'],
        'client_secret':oauthDict['app_secret'],
        'refresh_token':refresh_token,
        'grant_type':'refresh_token',
    }
    req = requests.post(token_url,data=data)
    print(json.loads(req.text))
    return json.loads(req.text)


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


def save_session(client,fileName):
    '''
    将授权信息保存到JSON文件中
    :param client:
    :param fileName:
    :return:
    '''
    client = refresh_token(client['refresh_token'])
    client.update({
        'panName':fileName,
        'expires_set':int(time()),
        'is_sharePoint':False,
        'panFrom':'oneDrive',
    })

    # 转成json对象并保存
    with open(os.path.join(BASE_DIR, 'driveJsons', '%s.json'%fileName), "w+") as session_file:
        json.dump(client, session_file)

    return client

def load_session(status_dict):
    '''
    将传入的字典对象转为OD的client
    :param status_dict:
    :return: dict->OneDriveClient
    '''
    # json_file_to_dict
    pass

if __name__ == '__main__':
    print(save_session(client,'nya'))
