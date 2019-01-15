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

