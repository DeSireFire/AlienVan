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
    print(BaseUrl)
    return BaseUrl

def reduce_odata(odatavalue):
    '''
    简化odata,提取需要的常用键值对
    :param odata: 字典，od返回的文件列表数据,键'value'
    :return: dict->dict
    '''
    mineType = lambda x:x['file']['mimeType'] if 'file' in x.keys() else '文件夹'  # 文件类型判断
    childCount = lambda x:x['folder']['childCount'] if 'folder' in x.keys() else ''  # 文件子项
    thumbnails = lambda x:x['thumbnails'] if 'thumbnails' != [] else ''  # 文件缩略图不为空
    from odTools.otherHandler import fileIco
    temp = {
        'id':odatavalue['id'],  # 文件id
        'name':odatavalue['name'],  # 文件名
        'size':odatavalue['size'],  # 文件大小
        'mimeType':mineType(odatavalue),  # 类型
        'createdDateTime':odatavalue['createdDateTime'].replace('-','/').replace('T',' ').replace('Z',''),    # 创建日期
        'lastModifiedDateTime':odatavalue['lastModifiedDateTime'].replace('-','/').replace('T',' ').replace('Z',''),  # 修改日期
        'childCount':str(childCount(odatavalue)),  # 内含子项数
        'parentID':odatavalue['parentReference']['id'],  # 父级目录id
        'parentRoot':odatavalue['parentReference']['path'][12:],  # 父级目录路径
        'thumbnails':thumbnails(odatavalue),  # 文件缩略图
        'fileIco':fileIco(mineType(odatavalue)),  # 文件缩略图
    }
    # print(temp['mimeType'],temp['name'],temp['fileIco'],)
    return temp



# 操作函数
def files_list(client,od_type,path=''):
    '''
    文件列表查询
    :param od_type: 布尔，onedrive 类型
    :param path: 字符串，目标目录名
    :return:
    '''

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(client["access_token"])}
    get_res = requests.get(typeURL(client,od_type,path), headers=headers, timeout=30, verify=False)
    get_res = json.loads(get_res.text)
    print(get_res)
    for i in get_res:
        print('%s:%s'%(i,get_res[i]))
        if i == 'value':
            for n in get_res[i]:
                print(n)
    return get_res


def new_folder(client, fileName, parent_id='root'):
    '''
    创建新目录
    :param fileName: 字符串，新建目录名
    :param parent_id: 字符串，父目录的id
    :return:
    '''
    url = client['app_url'] + '/v1.0/me/drive/{}/children'.format(parent_id)

    headers = {'Authorization': 'bearer {}'.format(client["access_token"]), 'Content-Type': 'application/json'}
    payload = {
        "name": fileName,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename"
    }
    get_res = requests.post(url, headers=headers, data=json.dumps(payload))
    get_res = json.loads(get_res.text)
    print(get_res)
    for i in get_res:
        print('%s:%s'%(i,get_res[i]))
        if i == 'value':
            for n in get_res[i]:
                print(n)
    return get_res


def rename_files(client, fileid, new_name):
    '''
    重命名文件/目录
    :param client:字典
    :param new_name:
    :return:
    '''
    url = client['app_url'] + '/v1.0/me/drive/items/{}'.format(fileid)
    headers = {'Authorization': 'bearer {}'.format(client["access_token"]), 'Content-Type': 'application/json'}
    payload = {"name": new_name}
    get_res = requests.patch(url, headers=headers, data=json.dumps(payload))
    get_res = json.loads(get_res.text)
    print(get_res)
    return get_res


def delete_files(client, fileid):
    '''
    删除文件/目录
    :param client:
    :param fileid: 文件/目录的id
    :return:
    '''
    url = client['app_url'] + '/v1.0/me/drive/items/{}'.format(fileid)
    headers = {'Authorization': 'bearer {}'.format(client["access_token"]), 'Content-Type': 'application/json'}
    get_res = requests.delete(url, headers=headers)
    print(get_res)
    return get_res


if __name__ == '__main__':
    pass
    # temp = flush_token(info["refresh_token"])

    # flist = od_filesList(temp,1)

    # folder_create(1,'','wori')

    # rename_files(temp,flist['value'][1]['id'],'rename2')

    # delete_files(temp,flist['value'][1]['id'])