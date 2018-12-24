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