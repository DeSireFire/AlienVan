'''
onedrive 授权登陆处理器
'''
from requests_oauthlib import OAuth2Session
import requests,json

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

