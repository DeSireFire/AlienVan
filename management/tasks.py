#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
import time
from celery.utils.log import get_task_logger
from alienVan.celery import app
# from odTools import authentication

from odTools.authentication import *

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
def authURL(init_type):
    '''
    异步获取注册链接
    :param init_type: 字符串，选择普通版或者商业版OD使用。
    :return: 字符串，授权登陆URL
    '''
    return getClient(init_type)

@app.task
def returnClient(code):
    '''
    返回onedrive client实例
    :param code: 字符串，onedive登陆授权码code
    :return: 返回onedrive client实例
    '''
    print('code : %s'%code)
    # return init_N(code)
    temp = init_N(code)
    # return 'nyanyan code : %s'%code
    return temp

@app.task
def loadSession(pathFileName):
    from odTools.session import load_session
    import json
    import logging
    # temp = load_session(pathFileName)
    try:
        with open(pathFileName, "r") as session_file:
            status_dict = json.load(fp=session_file)
    except IOError as e:
        logging.fatal(e.strerror)
        logging.fatal('无法读取到session文件!')
        exit()
    return status_dict