#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
import time
from celery.utils.log import get_task_logger
from alienVan.celery import app

from odTools.authentication import *

@app.task
def test(x, y):
   print('nya nya ok!')
   print(x)
   print(y)