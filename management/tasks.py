#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
import time
from celery.utils.log import get_task_logger
from alienVan.celery import app
from odTools import authentication

from odTools.authentication import *

@app.task
def test(x, y):
    x = int(x)+2
    y = int(y)+3
    # return x+y

# @app.task
# def