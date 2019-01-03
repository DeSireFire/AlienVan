'''
onedrive 授权登陆处理器
'''
from requests_oauthlib import OAuth2Session
import requests,json
from alienVan.appConfig import token_url,oauthDict,authorize_url
import logging
from time import time
from odTools.otherHandler import *
from alienVan.settings import BASE_DIR

# auth 授权登陆


def get_sign_in_url():
    '''
    初始化OA链接
    :return:None->str*2
    '''
    new_auth = OAuth2Session(oauthDict['app_id'],
    scope=oauthDict['scopes'],
    redirect_uri=oauthDict['redirect'])
    sign_in_url, state = new_auth.authorization_url(authorize_url, prompt='login')
    return sign_in_url, state


def get_token_from_code(code):
    '''
    得到返回链接：https://github.com/DeSireFire/AlienVan?code=M4d63b8cd-2951-1a96-fe98-f186a5c6e302&state=a13ypG9SFzKej0tQXvBiD1QPt46x9v
    :param callback_url: 为示例链接里面的code
    :return:
    '''
    myheader = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    data = {
        'client_id':oauthDict['app_id'],
        'redirect_uri':oauthDict['redirect'],
        'client_secret':oauthDict['app_secret'],
        'code':code,
        'grant_type':'authorization_code',
    }
    rep = requests.post(token_url,headers = myheader,data=data)
    client = json.loads(rep.text)
    client.update({
        'expires_set': time(),
        'panFrom': 'oneDrive',
    })
    return client






# Session 维护


def refresh_token(client):
    '''
    刷新客户端的token。
    一个令牌的默认过期时间为3600秒。
    获取将与所有请求一起使用的访问令牌，需要授权。
    这只是帮助自定义的辅助函数，下载和上传。
    :return: OneDriveClient->OneDriveClient
    :param client: 字典，链接信息
    :return:
    '''
    data = {
        'client_id': oauthDict['app_id'],
        'redirect_uri': oauthDict['redirect'],
        'client_secret': oauthDict['app_secret'],
        'refresh_token': client['refresh_token'],
        'grant_type': 'refresh_token',
    }
    req = requests.post(token_url, data=data)
    client.update(json.loads(req.text))
    client.update({
        'expires_set': time(),
        'panFrom': 'oneDrive',
    })
    return client


def token_time_to_live(client):
    '''
    以秒为单位获取令牌的到期时间。
    必须确保令牌可用。
    :param client:
    :return: OneDriveClient->bool
    '''
    print(int(client['expires_set'] - time()))
    if int(client['expires_set'] - time()) > 3000 or int(client['expires_set'] - time()) < 0:
        return True
    else:
        return False


def save_session(client, fileName):
    '''
    将授权信息保存到JSON文件中
    :param client:
    :param fileName:
    :return:
    '''
    # 转成json对象并保存
    if 'error' not in client.keys():
        with open(os.path.join(BASE_DIR, 'driveJsons', '%s.json' % fileName), "w+") as session_file:
            json.dump(client, session_file)

        return client


def load_session(pathFileName):
    '''
    将传入的字典对象转为OD的client
    :param fileName:字符串，对应的json文件夹名
    :return: dict->OneDriveClient
    '''

    # print(fileList(os.path.join(BASE_DIR, 'driveJsons'), '.json'))
    client = json_file_to_dict(pathFileName)
    if token_time_to_live(client):
        print('需要刷新')
        client = refresh_token(client)
        save_session(client,pathFileName.split('/')[-1].split('.')[0])
        return client
    else:
        return client

if __name__ == '__main__':
    pass
    # print(authorize_url)
    # print(token_url)
    # sign_in_url,state = get_sign_in_url()
    # print(sign_in_url)
    # print(state)
    # code = input('code:')
    # temp = get_token_from_code(code)
    # flush_token(temp['refresh_token'])

    # print(save_session(client,'nya'))
    print(load_session('/home/rq/workspace/python/AlienVan/driveJsons/anime.json'))