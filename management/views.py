from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import json

# Create your views here.
# 左导航选项控制[[选项名，次级菜单列表，选项前小图标],[选项名，是否包含次级菜单，选项前小图标]]
Sidebar = [
    ['网盘组状态',['硬盘组 1','硬盘组 2'],'fa fa-edit'],
    ['网盘载入',False,'fa fa-edit'],
    ['数据库设置',False,'fa fa-edit'],
    ['Aria2工具',False,'fa fa-edit'],
    ['主题设置',False,'fa fa-edit'],
]

def test(request):
    return render(request, 'theme_AdminLTE/management/base_sec.html')

def addPan(request):
    from odTools.authHandler import get_sign_in_url
    sign_in_url, state = get_sign_in_url()
    context = {
        'title':'管理-网盘载入',
        'sidebar':sidebar_list('网盘组状态'),    # 左导航条
        'pageHeader':'网盘载入',   # 选项卡标题
        'Level':'网盘载入',  # 面包屑次级
        'Here':'网盘载入',  # 面包屑次级
        'pageHeaderSmall':'没有载入网盘，就什么也做不了..emmmmm',
        'authUrl':sign_in_url,
        'info':'',
    }
    if 'code' in request.GET and request.GET['code']:  # 获得用户输入值
        driveInfo = {
            'panName':request.GET.get('panName'),
            'code':request.GET.get('code'),
            'odtype':request.GET.get('odtype'),
        }
        for i in driveInfo:
            if driveInfo[i]:
                context['info'] = '信息不完整，要填完哦'

                return render(request, 'theme_AdminLTE/management/loadDrive.html',context)

        # from .tasks import getAuth
        # client = getAuth.delay(driveInfo).get()
        # print(client)
        context['info'] = '添加成功～'
        return render(request, 'theme_AdminLTE/management/dashBoard.html', context)

    return render(request, 'theme_AdminLTE/management/loadDrive.html',context)

def panAction(request):
    context = {
        'title':'管理-网盘状态',
        'sidebar':sidebar_list('网盘组状态'),    # 左导航条
        'pageHeader':'管理-网盘状态',   # 选项卡标题
        'Level':'网盘状态',  # 面包屑次级
        'Here':'',  # 面包屑次级
        'pageHeaderSmall':'',
        'info':{'wo':'233','wo2':'233','wo3':'233'},
    }
    # 读取 session 的 json 文件
    # from .tasks import loadSession
    # temp = loadSession('/home/rq/workspace/python/AlienVan/driveJsons/anime.json')
    # context['Here'] = temp['panName']

    # temp = loadSession.delay('/home/rq/workspace/python/AlienVan/driveJsons/anime.json').get()
    # from odTools.filesHandler import files_list
    # fl = files_list(temp,1,'')
    # print(fl)
    # context['info'] = fl['value']
    # sign_in_url, state = get_sign_in_url()
    # context['temp'] = sign_in_url

    return render(request, 'theme_AdminLTE/management/dashBoard.html', context)

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


def sidebar_list(active):
    temp = []
    htmlDict = {
        'li':'<li class="{active}"><a href="#"><i class="{i}"></i> <span>{name}</span></a></li>',
        'menuLi':'<li><a href="#">{}</a></li>',
        'treeview':'<li class="treeview active"><a href="#"><i class="{i}"></i> <span>{name}</span><span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span></a><ul class="treeview-menu">{li}</ul></li>',
    }
    for i in Sidebar:
        if i[0] == active:
            if i[1]:
                tempStr = htmlDict['treeview'].format(active='active',i=i[2],name=i[0],li=''.join([htmlDict['menuLi'].format(x) for x in i[1]]))
            else:
                tempStr = htmlDict['li'].format(active='active',i=i[2],name=i[0])
        else:
            if i[1]:
                tempStr = htmlDict['treeview'].format(active='',i=i[2],name=i[0],li=''.join([htmlDict['menuLi'].format(x) for x in i[1]]))
            else:
                tempStr = htmlDict['li'].format(active='', i=i[2], name=i[0])
        temp.append(tempStr)
    return ''.join(temp)


from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

if __name__ == '__main__':
    # from management.tasks import test
    # a = test.delay(1,2).get()
    # print(a)
    pass