'''
onedrive 上传文件
'''
import onedrivesdk



# 上传
def uploader_test(client, item_id, pathFile):
    '''
    简单的上传文件
    :param item_id: 字符串，上传的目标目录名
    :param pathFile: 字符串，待上传的文件和其地址
    :return:
    '''
    fileName = pathFile.split('/')[-1]
    return client.item(drive='me', id=item_id).children['fileName'].upload(pathFile)

if __name__ == '__main__':
    uploader_test(233,233,'/home/rq/workspace/python/AlienVan/README.md')