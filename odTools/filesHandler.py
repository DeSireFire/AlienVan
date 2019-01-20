'''
onedrive 文件操作工具箱
'''
import requests,json,os


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

def reduce_odata(odatavalue,keyName = None):
    '''
    简化odata,提取需要的常用键值对
    :param odata: 字典，od返回的文件列表数据,键'value'
    :param keyName: 字符串，需要特殊提取的odata键名
    :return: dict->dict
    '''
    get_keyName = lambda x:x[keyName] if keyName in x.keys() else []  # 获取特殊键
    mineType = lambda x:x['file']['mimeType'] if 'file' in x.keys() else '文件夹'  # 文件类型判断
    childCount = lambda x:x['folder']['childCount'] if 'folder' in x.keys() else ''  # 文件子项
    thumbnails = lambda x:x['thumbnails'] if 'thumbnails' != [] and 'file' in x.keys() else ''  # 文件缩略图不为空
    download = lambda x:x['@microsoft.graph.downloadUrl'] if '@microsoft.graph.downloadUrl' in x.keys() else ''  # 文件缩略图不为空
    from generalTs.otherHandler import fileIco,fileSize
    temp = {
        'id':odatavalue['id'],  # 文件id
        'name':odatavalue['name'],  # 文件名
        'size':fileSize(odatavalue['size']),  # 文件大小
        'mimeType':mineType(odatavalue),  # 类型
        'createdDateTime':odatavalue['createdDateTime'].replace('-','/').replace('T',' ').replace('Z',''),    # 创建日期
        'lastModifiedDateTime':odatavalue['lastModifiedDateTime'].replace('-','/').replace('T',' ').replace('Z',''),  # 修改日期
        'childCount':str(childCount(odatavalue)),  # 内含子项数
        'parentID':odatavalue['parentReference']['id'],  # 父级目录id
        'parentRoot':odatavalue['parentReference']['path'][12:],  # 父级目录路径
        'thumbnails':thumbnails(odatavalue),  # 文件缩略图
        'fileIco':fileIco(mineType(odatavalue)),  # 文件图标
        'download':download(odatavalue),  # 文件下载链
        }
    if keyName:
        temp[keyName] = get_keyName(odatavalue)
    # print(temp['mimeType'],temp['name'],temp['fileIco'])
    return temp

def filter_files(client,nameKey,filterStr='file ne null',parent_id='root'):
    '''
    文件过滤,过滤语法
    https://docs.microsoft.com/en-us/onedrive/developer/rest-api/concepts/filtering-results?view=odsp-graph-online
    :param nameKey: 文件名关键字
    :return:
    '''
     # 查询文件名包含.jpg"且image类型不为 null" 的所有子项
    from alienVan.appConfig import oauthDict
    url = oauthDict['app_url'] + "/v1.0/me/drive/{parent_id}/search(q='{nameKey}')".format(
        parent_id=parent_id,
         nameKey=nameKey,)
    headers = {'Authorization': 'bearer {}'.format(client["access_token"])}
    get_res = requests.get(url, headers=headers, verify=False)
    get_res = json.loads(get_res.text)
    print(get_res)
    return get_res


# 操作函数
def files_list(client,od_type,path=''):
    '''
    文件列表获取
    :param od_type: 布尔，onedrive 类型
    :param path: 字符串，目标目录名
    :return:
    '''

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(client["access_token"])}
    get_res = requests.get(typeURL(client,od_type,path), headers=headers, timeout=30, verify=False)
    get_res = json.loads(get_res.text)
    # print(get_res)
    # for i in get_res:
    #     print('%s:%s'%(i,get_res[i]))
    #     if i == 'value':
    #         for n in get_res[i]:
    #             print(n)
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
    from alienVan.appConfig import oauthDict
    url = oauthDict['app_url'] + '/v1.0/me/drive/items/{}'.format(fileid)
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
    #todo 待优化,错误信息检查和返回信息
    from alienVan.appConfig import oauthDict
    url = oauthDict['app_url'] + '/v1.0/me/drive/items/{}'.format(fileid)
    headers = {'Authorization': 'bearer {}'.format(client["access_token"]), 'Content-Type': 'application/json'}
    get_res = requests.delete(url, headers=headers, verify=False)
    print(get_res)

    return get_res

def all_images(client,path='root'):
    '''
    统计所有图片文件
    :param client:
    :param path:
    :return:
    '''
    imageType = ['.gif', '.jpg', '.png', '.webp',]
    imageRes = {
        '.gif':{'count':0,'resSize':0},# 文件数量，文件大小总和
        '.jpg':{'count':0,'resSize':0},
        '.png':{'count':0,'resSize':0},
        '.webp':{'count':0,'resSize':0},
        'Res':{'count':0,'resSize':0},# 所有图片文件的数量和大小总和
    }
    # 商业版OD不支持createdDateTime 以外的过滤语法，垃圾。
    from generalTs.otherHandler import fileSize
    for i in imageType:
        temp = filter_files(client, i, filterStr='image%20ne%20null%20and%20file%20ne%20null', parent_id='root')

        # 请求出错
        if 'value' not in temp.keys() or ['value']=={}:
            continue
        for n in temp['value']:
            # 排除文件名带关键字但不是图片文件的文件
            if 'image' in n['file']['mimeType'] or '.webp' == os.path.splitext(n['name'])[1]:
                imageRes[i]['count'] += 1
                imageRes[i]['resSize'] += int(n['size'])

        imageRes['Res']['count'] += imageRes[i]['count']
        imageRes['Res']['resSize'] += imageRes[i]['resSize']

        imageRes[i]['resSize'] = fileSize(imageRes[i]['resSize'])
    imageRes['Res']['resSize'] = fileSize(imageRes['Res']['resSize'])
    return imageRes

def all_video(client,path='root'):
    '''
    统计所有视频文件
    :param client:
    :param path:
    :return:
    '''
    tempType = ['.avi','.mp4','.mkv','.flv','.rm',]
    tempRes = {
        '.avi':{'count':0,'resSize':0},# 文件数量，文件大小总和
        '.mp4':{'count':0,'resSize':0},
        '.mkv':{'count':0,'resSize':0},
        '.flv':{'count':0,'resSize':0},
        '.rm':{'count':0,'resSize':0},
        'Res':{'count':0,'resSize':0},# 所有图片文件的数量和大小总和
    }
    # 商业版OD不支持createdDateTime 以外的过滤语法，垃圾。
    from generalTs.otherHandler import fileSize
    for i in tempType:
        temp = filter_files(client, i, filterStr='image%20ne%20null%20and%20file%20ne%20null', parent_id='root')

        # 请求出错
        if 'value' not in temp.keys() or ['value']=={}:
            continue
        for n in temp['value']:
            # 排除文件名带关键字但不是图片文件的文件
            if 'video' in n['file']['mimeType']:
                tempRes[i]['count'] += 1
                tempRes[i]['resSize'] += int(n['size'])

        tempRes['Res']['count'] += tempRes[i]['count']
        tempRes['Res']['resSize'] += tempRes[i]['resSize']

        tempRes[i]['resSize'] = fileSize(tempRes[i]['resSize'])
    tempRes['Res']['resSize'] = fileSize(tempRes['Res']['resSize'])
    print(tempRes)
    return tempRes


if __name__ == '__main__':
    pass
    from odTools.authHandler import load_session
    from alienVan.settings import BASE_DIR
    pathFileName = os.path.join(BASE_DIR, 'driveJsons', 'msDiskOne.json')
    CLIENT = load_session(pathFileName)
    # all_images(CLIENT)
    all_video(CLIENT)

    # from odTools.authHandler import refresh_token
    # temp = refresh_token(info["refresh_token"])

    # flist = od_filesList(temp,1)

    # folder_create(1,'','wori')

    # rename_files(temp,flist['value'][1]['id'],'rename2')

    # delete_files(temp,flist['value'][1]['id'])
