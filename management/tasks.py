#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
import time
from celery.utils.log import get_task_logger
from alienVan.celery import app
# from odTools import authentication

from odTools.authentication import *
from odTools.authHandler import *

@app.task
def test(x, y):
    '''
    celery 可以返回字典，字符串，数字。
    celery 调用task里的函数，print是无法直接看见的。
    只会保存return的结果到backend
    TypeError("Object of type 'OneDriveClient' is not JSON serializable",)
    od对象无法直接保存到backend,需要转化成字典这种可以保存成json的对象
    '''
    print('日狗了!怎麼回事')
    import json
    temp = json.dumps({'x': x, 'y': y})
    print(type(temp))
    return temp
    # return {'x': x, 'y': y}

@app.task
def odtest(init_type):
    return getClient(init_type)

@app.task
def getAuth(driveInfo):
    '''
    异步获取注册链接
    :param init_type: 字符串，选择普通版或者商业版OD使用。
    :return: 字符串，授权登陆URL
    '''
    temp = get_token_from_code(driveInfo['code'])
    temp.update(driveInfo)
    save_session(temp,driveInfo['panName'])
    return temp

@app.task
def returnfileList(client):
    '''
    返回onedrive client实例
    :param client:
    :return: 返回onedrive client实例
    '''
    temp = fileList(os.path.join(BASE_DIR, 'driveJsons'), '.json')
    return temp

@app.task
def loadSession(pathFileName):
    return load_session(pathFileName)

@app.task
def returnPanNames():
    temp = []
    for i in fileList(os.path.join(BASE_DIR, 'driveJsons'), '.json'):
        temp.append(os.path.splitext(i)[0].split('/')[-1])
    return temp

if __name__ == '__main__':
    print(returnPanNames())