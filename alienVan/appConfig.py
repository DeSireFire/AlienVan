# global  redirect_uri, client_secret, client_id, api_base_url, scopes, discovery_uri, auth_server_url, auth_token_url
# api用例参考
# If you are not sure whether this is safe,
# you can register your own APP and use your own URL.
# Don't just change it: you will have error.
redirect_uri = 'https://od.cnbeining.com'

## Normal
client_secret_normal = 'o.+2TBy+7-ijKLMl05spsohdx464OtwU'
client_id_normal = 'e2d585cd-751f-4c7e-aab7-d8b48c485f94'
api_base_url = 'https://api.onedrive.com/v1.0/'
scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

## Business
discovery_uri = 'https://api.office.com/discovery/'
auth_server_url = 'https://login.microsoftonline.com/common/oauth2/authorize',
auth_token_url = 'https://login.microsoftonline.com/common/oauth2/token'

# If you are working with Office 365 you may want to create your own app
# and change the following:
# You can still use https://od.cnbeining.com as redirect URL.
client_id_business = '6fdb55b4-c905-4612-bd23-306c3918217c'
client_secret_business = 'HThkLCvKhqoxTDV9Y9uS+EvdQ72fbWr/Qrn2PFBZ/Ow='


'''
接口信息
'''

oauthDict = {
    'app_id':'11b16c5c-3451-4706-96ec-b503b865c256',
    'app_secret':'V/FI*4yV.?vnVI4j6giEooD48NfyTfKm',
    'redirect':'https://od.cnbeining.com',
    'scopes':['Files.ReadWrite', 'User.Read', 'offline_access','openid'],
    'authority':'https://login.microsoftonline.com/common',
    'authorize_endpoint':'/oauth2/v2.0/authorize',
    'token_endpoint':'/oauth2/v2.0/token',
    'app_url':"https://graph.microsoft.com/",
}
authorize_url = '{0}{1}'.format(oauthDict['authority'], oauthDict['authorize_endpoint'])    # https://login.microsoftonline.com/common/oauth2/v2.0/authorize
token_url = '{0}{1}'.format(oauthDict['authority'], oauthDict['token_endpoint'])    # https://login.microsoftonline.com/common/oauth2/v2.0/token

