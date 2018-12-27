'''
onedrive 文件操作工具箱
'''
import requests,json


# 通用函数
def typeURL(client,od_type,path=''):
    '''
    是否为特殊版本的onedrive，并返回对应的app_base URL
    :param od_type: 布尔值，真为普通版，假为特殊版
    :return: bool->str
    '''
    from alienVan.appConfig import oauthDict
    app_url = oauthDict['app_url']
    if od_type:
        app_url = app_url+"/v1.0/me/drive"
    else:
        app_url = "https://{}-my.sharepoint.cn/_api/v2.0/me/drive".format(client['other'])
    if path:
        BaseUrl = app_url + '/root:{}:/children?expand=thumbnails'.format(path)
    else:
        BaseUrl = app_url + '/root/children?expand=thumbnails'

    return BaseUrl



# 操作函数
def filesList(client,od_type,path=''):
    '''
    文件列表查询
    :param od_type: 布尔，onedrive 类型
    :param path: 字符串，目标目录名
    :return:
    '''

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(client["access_token"])}
    get_res = requests.get(typeURL(client,1,''), headers=headers, timeout=30)
    get_res = json.loads(get_res.text)
    print(get_res)
    for i in get_res:
        print('%s:%s'%(i,get_res[i]))
        if i == 'value':
            for n in get_res[i]:
                print(n)
    return get_res

if __name__ == '__main__':
    pass