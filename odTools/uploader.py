'''
onedrive 上传文件
'''
import requests,json
from alienVan.appConfig import oauthDict
import os.path

## 上传总函数

def main_uploader(client,filePath,remotePath,fileid=False):
    '''上传文件，总函数
    :param filePath:str,上传的目标文件在本地的完整路径
    :param remotePath:str,远程网盘要放的路径
    '''

    # 如果存在文件id,则使用文件更新已有项目
    if fileid:
        return updater(client, fileid,filePath)

    # 小于8MB用小文件上传
    if os.path.getsize(filePath) < 8388608:
        return small_uploader(client,filePath,remotePath)
    else:   # 大于8mb用大文件上传
        return big_uploader(client,os.path.basename(filePath),remotePath)



## 上传函数

def updater(client,fileid,filePath):
    '''更新上传已有项目
    PUT /me/drive/items/{item-id}/content
    '''
    url = oauthDict['app_url'] + '/v1.0/me/drive/items/{}/content'.format(fileid)
    headers = {'Authorization': 'bearer {}'.format(client["access_token"])}
    pull_res = requests.put(url, headers=headers, data=open(filePath, 'rb'))
    pull_res = json.loads(pull_res.text)
    return pull_res

def small_uploader(client,filePath,remotePath):
    '''上传新项目
    PUT /me/drive/items/{parent-id}:/{filename}:/content

    PUT /me/drive/root:/FolderA/FileB.txt:/content??
    两者都可以


    坑逼微软api，你奶奶的,↓根本不用写好不
    Content-Type: text/plain

    '''
    fileName = os.path.basename(filePath)
    url = oauthDict['app_url'] + '/v1.0/me/drive/items/root:/{remotePath}{fileName}:/content'.format(remotePath=remotePath+'/',fileName=fileName)
    headers = {'Authorization': 'bearer {}'.format(client["access_token"])}
    pull_res = requests.put(url, headers=headers, data=open(filePath, 'rb'), verify=False)
    pull_res = json.loads(pull_res.text)

    return {"status":"ok","info":pull_res,"percent": "100%"}

def big_uploader(client,filePath,remotePath):
    '''
    上传大文件
    :param filePath:str,上传的目标文件在本地的完整路径
    :param remotePath:str,远程网盘要放的路径
    '''
    import os.path
    # 创建上传会话，获取上传URL
    sessionInfo = uploader_creatSession(client,os.path.basename(filePath),remotePath)

    # 目标文件分段
    #todo fileRuler可以写活而不用固定长度
    fileSize = os.path.getsize(filePath)
    fileRuler = 10485760    # 10MB 尺
    listSlice = [[i, i + fileRuler - 1, fileRuler] for i in range(0, fileSize, fileRuler)] # 生成切好的分段组数
    # 对齐末尾剩余的文件片段
    listSlice[-1] =[listSlice[-1][0],   # setPoint
        fileSize-1 if listSlice[-1][1]>fileSize else listSlice[-1][1],  # endPoint
        fileSize % fileRuler if listSlice[-1][1]>fileSize else listSlice[-1][2]] # Content-Length

    # 分段上传的头部base
    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': '',   # 上传片段的长度
        'Content-Range': ''  # 下一次上传，endPoint等于setPoint+新读取的片段长度-1
    }

    # 遍历分段
    for i in listSlice:
        # 构造新的分段头部
        headers['Content-Length'] = str(i[2])
        headers['Content-Range'] = 'bytes {setPoint}-{endPoint}/{fullLen}'.format(setPoint=i[0],endPoint=i[1],fullLen=fileSize)    # 下一次上传，endPoint等于setPoint+新读取的片段长度-1
        # 上传
        uploaderPart = requests.put(sessionInfo['uploadUrl'], headers=headers, data=uploader_fileSlice(filePath,i[0],i[2]))
        if uploaderPart.status_code in [200,201,202,204]:
            if uploaderPart.status_code == 201:  # 201 表示上传完成
                return {"status":"ok","info":json.loads(uploaderPart.text),"percent": "100%"}
            else:
                print({"status":"uploading","info":"","percent": '{:.0%}'.format(int(json.loads(uploaderPart.text)['nextExpectedRanges'][0].split('-')[0])/fileSize)})
                # return {"status":"uploading","info":"","percent": '{:.0%}'.format(int(json.loads(uploaderPart.text)['nextExpectedRanges'][0].split('-')[0])/fileSize)}

        else:
            print('发生错误')
            print(i)
            print(headers)
            print(uploaderPart.status_code)
            print(json.loads(uploaderPart.text))
            print(uploaderPart.status_code)


## 上传辅助函数

def uploader_creatSession(client,fileName,remotePath="/"):
    '''
    创建上传会话，获取上传URL
    :param fileName:str,文件名
    :param remotePath:str,远程网盘要放的路径
    '''
    url = oauthDict['app_url'] + '/v1.0/me/drive/root:/{}/{}:/createUploadSession'.format(remotePath,fileName)
    print(url)
    headers = {'Authorization': 'bearer {}'.format(client["access_token"]), 'Content-Type': 'application/json'}
    data = {
        "item": {
            "@microsoft.graph.conflictBehavior": "fail",    # 冲突行为属性,即是如果出现文件冲突则返回失败

            # "@microsoft.graph.conflictBehavior": "rename",    # 冲突行为属性,即是如果出现文件冲突则重命名

            # "@microsoft.graph.conflictBehavior": "replace",    # 冲突行为属性,即是如果出现文件冲突则替换
        }
    }
    pull_res = requests.post(url, headers=headers, data=json.dumps(data))
    print(json.loads(pull_res.text))
    if pull_res.status_code == 409:

        return False
    else:
        return json.loads(pull_res.text)


def uploader_fileSlice(filePath,setPoint,sliceLen):
    '''
    文件二进制切片
    :param filePath:
    :return:
    '''
    with open(filePath, 'rb') as f:
        f.seek(int(setPoint))   # 设置读取标头
        content = f.read(sliceLen)  # 从标头往后读取若干字节，不包括标头
    return content


if __name__ == '__main__':
    pass
    # temp = flush_token(info["refresh_token"])
    # big_uploader(temp,'test.zip','/')