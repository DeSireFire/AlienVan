from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import json

# Create your views here.

def test(request):
    return render(request, 'theme_AdminLTE/management/base_sec.html')

def home(request):
    context = {
        'title':'管理页',
        'temp':'',
    }
    # 读取 session 的 json 文件
    from .tasks import loadSession
    # temp = loadSession.delay('/home/rq/workspace/python/AlienVan/driveJsons/233.json').get()
    # print(temp)

    from odTools.authHandler import get_sign_in_url
    sign_in_url, state = get_sign_in_url()
    context['temp'] = sign_in_url
    return render(request, 'theme_simple/management/index.html', context)

def initBinding(request):
    '''

    :param odType: onedrive 类型 普通版或者商业版
    :return:2/89
    '''
    context = {
        'title': '授权地址页',
        'authURL':'',
    }
    init_type = request.GET.get('odType')
    from .tasks import authURL
    auth_url = authURL.delay(init_type).get()
    context['authURL'] = auth_url
    return render(request, 'management/index.html', context)

# csrf 例外
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def callBackBinding(request):
    print(str(request.body, encoding = "utf-8").split('&'))
    print(request.method)

    # 获取前端code
    code = request.POST.get('code')
    print(code)

    # code 传入 celery 返回字典化的session信息
    from .tasks import returnClient
    temp = returnClient.delay(code).get()
    print(temp)
    return HttpResponse(json.dumps(temp))



def ce_test(request):
    x = request.GET.get('x', '1')
    y = request.GET.get('y', '1')
    print(x,y)
    from .tasks import test
    a = test.delay(x,y).get()
    print(a)
    res = {'code': 200, 'message': 'ok', 'data': [a]}
    # res = {'code': 200, 'message': 'ok', 'data': [{'x': x, 'y': y}]}
    return HttpResponse(json.dumps(res))


def od_ce_test(request):
    x = request.GET.get('type', 'N')
    from .tasks import odtest
    a = odtest.delay(x).get()
    print('這裡是:'+a)
    res = {'code': 200, 'message': 'ok', 'data': [{'x': x}]}
    return HttpResponse(json.dumps(res))

if __name__ == '__main__':
    from management.tasks import test
    a = test.delay(1,2).get()
    print(a)
