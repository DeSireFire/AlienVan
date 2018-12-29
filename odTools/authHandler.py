'''
onedrive 授权登陆处理器
'''
from requests_oauthlib import OAuth2Session
import requests,json
from alienVan.appConfig import token_url,oauthDict,authorize_url




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
    print(json.loads(rep.text))
    return json.loads(rep.text)


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


if __name__ == '__main__':
    print(authorize_url)
    print(token_url)
    sign_in_url,state = get_sign_in_url()
    print(sign_in_url)
    print(state)
    code = input('code:')
    temp = get_token_from_code(code)
    # flush_token(temp['refresh_token'])