import sys
import os


def dict_merge(a, b):
    c = a.copy()
    c.update(b)
    return c

def fileList(path, fileType, listName=[]):
    '''
    读取指定目录下的文件名
    :param path: 需要检查的目录
    :param listName: 文件名列表已有
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
if __name__ == '__main__':
    from alienVan.settings import BASE_DIR
    print(os.path.join(BASE_DIR,'driveJsons'))
    a = fileList(os.path.join(BASE_DIR,'driveJsons'),'.json')
    print(a)