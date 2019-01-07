from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import json

# Create your views here.

#todo 盘符更新需要思路
# 左导航选项控制[[选项名，是否有次级菜单列表，选项前小图标,选项卡的URL]
Sidebar = [
    ['网盘组状态',[],'fa fa-dashboard',''],
    ['网盘列表',[],'fa fa-edit','pans'],
    ['网盘载入',False,'fa fa-edit','addpan'],
    ['数据库设置',False,'fa fa-circle-o',''],
    ['Aria2工具',False,'fa fa-circle-o',''],
    ['主题设置',False,'fa fa-circle-o',''],
]



def panAction(request):
    '''
    网盘状态视图
    :param panName:
    :return:
    '''
    context = {
        'title': '管理-网盘状态',
        'sidebar': sidebar_list('网盘状态','/manage/'),  # 左导航条
        'pageHeader': '管理-网盘状态',  # 选项卡标题
        'Level': '网盘状态',  # 面包屑次级
        'Here': '',  # 面包屑次级
        'pageHeaderSmall': '未发现挂载网盘',
        'info': '',
    }
    # 如果发现没有挂载网盘json文件，直接跳转网盘添加页
    from .tasks import returnPanNames
    pansName = returnPanNames() # 盘符列表
    if not pansName:
        return HttpResponseRedirect("addpan")

    # 检查panName 是否存在和存在于挂载网盘列表中
    if 'name' in request.GET and request.GET['name'] and request.GET['name'] in Sidebar[0][1]:  # 获得用户输入值
        context['Here'] = request.GET['name']
        context['pageHeaderSmall'] = request.GET['name']
    else:
        context['Here'] = pansName[0]
        context['pageHeaderSmall'] = pansName[0]
        # todo 添加更多   context


    return render(request, 'theme_AdminLTE/management/dashBoard.html', context)

def pans(request):
    '''
    网盘列表视图
    :param panName:
    :return:
    '''
    #todo 把读取方式改成celery
    #todo 添加前端列表超链接
    context = {
        'title':'管理-网盘列表',
        'sidebar':sidebar_list('网盘列表','/manage/'),    # 左导航条
        'pageHeader':'管理-网盘列表',   # 选项卡标题
        'Level':'网盘列表',  # 面包屑次级
        'Here':'',  # 面包屑次级
        'pageHeaderSmall':'',
        'info':'',
        'test':[233,666,777]
    }
    # 如果发现没有挂载网盘json文件，直接跳转网盘添加页
    from .tasks import returnPanNames
    pansName = returnPanNames() # 盘符列表
    if not pansName:
        return HttpResponseRedirect("addpan")

    # 检查panName 是否存在和存在于挂载网盘列表中
    if 'name' in request.GET and request.GET['name'] and request.GET['name'] in Sidebar[0][1]:  # 获得用户输入值
        context['Here'] = request.GET['name']
        context['pageHeaderSmall'] = request.GET['name']
    else:
        context['Here'] = pansName[0]
        context['pageHeaderSmall'] = pansName[0]
        # todo 添加更多   context

    # 读取 session 的 json 文件
    from .tasks import loadSession
    print('{}.json'.format(context['Here']))
    temp = loadSession('{}.json'.format(context['Here']))
    context['Here'] = temp['panName']

    # temp = loadSession.delay('/home/rq/workspace/python/AlienVan/driveJsons/anime.json').get()
    from odTools.filesHandler import files_list
    fl = files_list(temp,1,'')
    context['info'] = fl['value']

    return render(request, 'theme_AdminLTE/management/pans.html', context)

def addPan(request):
    '''
    添加网盘视图
    :return:
    '''
    from odTools.authHandler import get_sign_in_url
    sign_in_url, state = get_sign_in_url()
    context = {
        'title':'管理-网盘载入',
        'sidebar':sidebar_list('网盘载入','/manage/'),    # 左导航条
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
            if not driveInfo[i]:
                context['info'] = '信息不完整，要填完哦'

                return render(request, 'theme_AdminLTE/management/loadDrive.html',context)

        from .tasks import getAuth
        client = getAuth.delay(driveInfo).get()
        print(client)
        # context['info'] = '添加成功～'+client
        context['info'] = client

    return render(request, 'theme_AdminLTE/management/loadDrive.html',context)



# csrf 例外
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt

# 视图辅助函数


def sidebar_list(active,appURL=None):
    '''
    ⎛⎝≥⏝⏝≤⎠⎞
    :param active:
    :param appURL:
    :return:
    '''
    from .tasks import returnPanNames
    pansName = returnPanNames() # 盘符列表



    getValue = '#'  # 左导航下拉菜单超链接
    if appURL:
        getValue = '?name='


    htmlDict = {
        'li':'<li class="{active}"><a href="{url}"><i class="{i}"></i> <span>{name}</span></a></li>',
        'menuLi':'<li><a href="{url}">{text}</a></li>',
        'treeview':'<li class="treeview active"><a href="#"><i class="{i}"></i> <span>{name}</span><span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span></a><ul class="treeview-menu">{li}</ul></li>',
    }

    temp = []
    for i in Sidebar:
        menuLi = i[1]
        if i[1] == []:
            menuLi = pansName

        if i[0] == active:
            if menuLi:
                tempStr = htmlDict['treeview'].format(active='active',i=i[2],name=i[0],li=''.join([htmlDict['menuLi'].format(url=appURL+i[3]+getValue+x,text=x) for x in menuLi]))
            else:
                tempStr = htmlDict['li'].format(active='active',url=i[3],i=i[2],name=i[0])
        else:
            if menuLi:
                tempStr = htmlDict['treeview'].format(active='',i=i[2],name=i[0],li=''.join([htmlDict['menuLi'].format(url=appURL+i[3]+getValue+x,text=x) for x in menuLi]))
            else:
                tempStr = htmlDict['li'].format(active='',url=i[3],i=i[2],name=i[0])

        temp.append(tempStr)


    return ''.join(temp)


if __name__ == '__main__':
    # from management.tasks import test
    # a = test.delay(1,2).get()
    # print(Sidebar)
    pass