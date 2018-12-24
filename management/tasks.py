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
    print('日狗了!怎麼回事')
    print(x+y)
    return x+y

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
    return init_N(code)
