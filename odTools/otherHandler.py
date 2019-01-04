import sys
import os


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

def fileList(path,fileType,listName=[]):
    '''
    读取指定目录下的文件名
    :param path: 需要检查的目录
    :param listName: 已有的文件名列表，用于根新查找出来的列表合并
    :param fileType: 文件格式（后缀）
    :return: str->list
    '''
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            fileList(file_path,fileType,listName)
        elif os.path.splitext(file_path)[1]==fileType:
            listName.append(file_path)
    return listName


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
    from alienVan.settings import BASE_DIR
    print(os.path.join(BASE_DIR,'driveJsons'))
    a = fileList(os.path.join(BASE_DIR,'driveJsons'),'.json')
    print(a)