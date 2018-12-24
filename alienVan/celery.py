from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# 设置'celery'程序的默认Django设置模块。
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alienVan.settings')

app = Celery('alienVan')

# 在这里使用字符串意味着worker不必序列化
# 子进程的配置对象。
#  -  namespace ='CELERY'表示所有与芹菜相关的配置键
# 应该有一个`CELERY_`前缀。
app.config_from_object('django.conf:settings', namespace='CELERY')

# 如果在工程的应用中创建了tasks.py模块，那么Celery应用就会自动去检索创建的任务。比如你添加了一个任#务，在django中会实时地检索出来。
# 从所有已注册的Django app配置中加载任务模块。
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

'''
celery 常用方法
result = task.add.delay(10,20)  //调用函数和delay方法

result.get() //获取结果,timeout默认为0

result.ready() //如果函数执行出现阻塞则返回False，可进行判断！

result.get(propagate=False) // 如果出错，获取错误结果，不触发异常

result.traceback //打印异常详细结果

result.id //任务id

celery multi start name  project_name -l info //启动celery任务并后台运行

celery multi restart worker -A  celery_project //重新启动celery任务

celery multi stop worker //停止
'''