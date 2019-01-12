import sys
import os

def fileIco(mimeType):
    '''
    根据文件名，返回对应fa小图标
    :param mimeType: 字符串，oddata的 mimeType
    :return:
    '''
    if '文件夹' == mimeType:
        return 'fa-folder'
    elif 'video' in mimeType:
        return 'fa-film'
    elif 'audio' in mimeType:
        return 'fa-file-audio-o'
    elif 'txt' in mimeType:
        return 'fa-file-text-o'
    elif 'image' in mimeType:
        return 'fa-file-image-o'
    elif 'zip' in mimeType:
        return 'fa-file-zip-o'
    else:
        return 'fa-file-o'

def fileSize(sizeNumb):
    '''
    文件大小换算
    :param sizeNumb: int 数字
    :return:
    '''
    from hurry.filesize import size
    return size(int(sizeNumb))

def dict_merge(a, b):
    '''
    字典合并
    :param a:
    :param b:
    :return:
    '''
    c = a.copy()
    c.update(b)
    return c

def fileList(path,fileType):
    '''
    读取指定目录下的文件名
    :param path: 需要检查的目录
    :param fileType: 文件格式（后缀）
    :return: str->list
    '''
    temp = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            fileList(file_path,fileType)
        elif os.path.splitext(file_path)[1]==fileType:
            temp.append(file_path)
    return list(set(temp))

def fileWalk(path,fileType = None):
    '''
    列出所有文件，包括次级目录
    :param path:字符串，需要递归的路径
    :param fileType:字符串，需要递归的路径
    :var root:字符串，路径列表
    :var dirs:字符串，目录列表
    :var files:字符串，文件列表
    :return:
    '''
    temp = {
        'fileNames':[],# 文件名列表（有后缀）
        'files':[],# 文件名列表（无后缀）
        'rootfiles':[],# 绝对路径文件名列表
    }
    for root, dirs, files in os.walk(path, topdown=False):
        temp['fileNames']=files
        for name in files:
            temp['rootfiles'].append(os.path.join(root, name))
            if fileType in name and fileType != None:
                temp['files'].append(os.path.splitext(name)[0])
        for name in dirs:
            temp['rootfiles'].append(os.path.join(root, name))

    return temp

def dict_to_json_write_file(dictTemp,pathFileName):
    '''
    字典转json文本文件
    :param dictTemp: 字典，需要转换的字典
    :param pathFileName: 字符串，文件名和目录地址组成
    :return: dictTemp->json file
    '''
    import json
    if '.json' not in pathFileName:
        pathFileName = pathFileName+'.json'
    with open(pathFileName, 'w') as f:
        json.dump(dictTemp, f)  # 会在目录下生成一个json的文件，文件内容是dict数据转成的json数据

def json_file_to_dict(pathFileName):
    '''
    json文本文件读取并转为字典
    :param pathFileName: 字符串，文件名和目录地址组成,用于读取文件
    :return: json file->dictTemp
    '''
    import json
    try:
        with open(pathFileName, 'r') as f:
            dictTemp = json.loads(f.read().replace("'", '"'))
        return dictTemp
    except IOError as e:
        import logging
        logging.fatal(e.strerror)
        logging.fatal('无法读取到session文件!')
        exit()



if __name__ == '__main__':
    # from alienVan.settings import BASE_DIR
    # # print(os.path.join(BASE_DIR,'driveJsons'))
    # # a = fileList(os.path.join(BASE_DIR,'driveJsons'),'.json')
    # a = fileWalk(os.path.join(BASE_DIR,'driveJsons'),'.json')
    # print(a)
    print(fileSize(2333))