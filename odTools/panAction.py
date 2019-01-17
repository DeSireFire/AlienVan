import requests,json
from alienVan.appConfig import oauthDict

def get_driveInfo(client):
    '''
    获取od网盘信息
    :param client:
    :return:
    '''
    url = oauthDict['app_url'] + '/v1.0/me/drive/'
    headers = {'Authorization': 'bearer {}'.format(client["access_token"])}
    get_res = requests.get(url, headers=headers,verify=False)
    get_res = json.loads(get_res.text)
    return get_res

if __name__ == '__main__':
    pass