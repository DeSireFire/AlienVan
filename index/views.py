from django.shortcuts import render
from management.views import sidebar_list
from management.tasks import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

Sidebar = [
    ['网盘列表', [], 'fa fa-edit', 'pans'],
]

# Create your views here.
# def index(request):
#     """
#     响应首页
#     :param request:
#     :return:
#     """
#     context = {
#         'title': '次元圣经',
#         'novelTypes_html': [],
#         'novelTypes': [],
#     }
#
#     return render(request, 'index/index.html', context)


def index(request):
    '''
    网盘列表视图
    :param panName:
    :return:
    '''
    # todo 把读取方式改成celery
    context = {
        'title': '管理-网盘列表',
        'sidebar': sidebar_list('网盘列表', '/'),  # 左导航条
        'pageHeader': '管理-网盘列表',  # 选项卡标题
        'Level': '网盘列表',  # 面包屑次级
        'Here': '',  # 面包屑次级
        'pageHeaderSmall': '',
        'files': '',
        'goback': '',
    }
    # 如果发现没有挂载网盘json文件，直接跳转网盘添加页
    pansName = returnPanNames()  # 盘符列表
    if not pansName:
        return HttpResponseRedirect("addpan")

    # 检查panName 是否存在和存在于挂载网盘列表中
    if 'name' in request.GET and request.GET['name'] and request.GET['name'] in pansName:  # 获得用户输入值
        context['Here'] = request.GET['name']
        context['pageHeaderSmall'] = request.GET['name']
    else:
        context['Here'] = pansName[0]
        context['pageHeaderSmall'] = pansName[0]

    # 读取 session 的 json 文件
    from management.tasks import loadSession
    temp = loadSession('{}.json'.format(context['Here']))
    context['Here'] = temp['panName']

    # temp = loadSession.delay('/home/rq/workspace/python/AlienVan/driveJsons/anime.json').get()
    from odTools.filesHandler import files_list, reduce_odata
    # 获取需要请求的od路径
    fp = ''
    if 'path' in request.GET and request.GET['path']:
        fp = request.GET['path']
        context['goback'] = '/'.join(request.GET['path'].split('/')[0:-1])  # 返回od上一级路径

    fl = files_list(temp, 1, fp)  # 向od获取odata,文件列表信息需要时间

    context['files'] = [reduce_odata(x) for x in fl['value']]

    return render(request, 'theme_AdminLTE/index/pans.html', context)


def fileShow(request):
    '''
    文件浏览视图
    :return:
    '''
    context = {
        'title': '管理-文件浏览',
        'sidebar': sidebar_list('网盘列表', '/'),  # 左导航条
        'pageHeader': '管理-文件浏览',  # 选项卡标题
        'pageHeaderSmall': '你是在逗我开心对吗？',
        'Level': '网盘列表',  # 面包屑次级
        'Here': '',  # 面包屑次级
        'file': '',
        'urlDict': '',
        'panName': '',
    }
    if 'path' in request.GET and request.GET['path'] and 'name' in request.GET and request.GET['name']:

        # 读取 session 的 json 文件
        from management.tasks import loadSession
        temp = loadSession('{}.json'.format(request.GET['name']))
        context['Here'] = temp['panName']
        context['panName'] = temp['panName']
        # 获取对应文件名信息
        from odTools.filesHandler import files_list, reduce_odata
        for i in [reduce_odata(x, 'createdBy') for x in
                  files_list(temp, 1, '/'.join(request.GET['path'].split('/')[0:-1]))['value']]:
            if i['name'] == request.GET['path'].split('/')[-1]:
                context['file'] = i
                # 通过文件类型构造各类引用链接
                if 'image' in i['mimeType']:
                    context['urlDict'] = {
                        '图片 分享': i['thumbnails'][0]['large']['url'],
                        'html 引用': '<img src="{}">'.format(i['thumbnails'][0]['large']['url']),
                        'Markdown 引用': '![{name}]({url})'.format(name=i['name'],
                                                                 url=i['thumbnails'][0]['large']['url']),
                    }
                elif 'text' in i['mimeType']:

                    context['urlDict'] = {
                        '文本 分享': i['download'],
                        'html 引用': i['download'],
                    }

                break

    return render(request, 'theme_AdminLTE/index/itemInfo.html', context)


def sidebar_list(active, appURL=None):
    '''
    ⎛⎝≥⏝⏝≤⎠⎞
    :param active:
    :param appURL:
    :return:
    '''
    pansName = returnPanNames()  # 盘符列表

    getValue = '#'  # 左导航下拉菜单超链接
    if appURL:
        getValue = '?name='

    htmlDict = {
        'li': '<li class="{active}"><a href="{url}"><i class="{i}"></i> <span>{name}</span></a></li>',
        'menuLi': '<li><a href="{url}">{text}</a></li>',
        'treeview': '<li class="treeview active"><a href="#"><i class="{i}"></i> <span>{name}</span><span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span></a><ul class="treeview-menu">{li}</ul></li>',
    }

    temp = []
    for i in Sidebar:
        menuLi = i[1]
        if i[1] == []:
            menuLi = pansName

        if i[0] == active:
            if menuLi:
                tempStr = htmlDict['treeview'].format(active='active', i=i[2], name=i[0], li=''.join(
                    [htmlDict['menuLi'].format(url=appURL + i[3] + getValue + x, text=x) for x in menuLi]))
            else:
                tempStr = htmlDict['li'].format(active='active', url=i[3], i=i[2], name=i[0])
        else:
            if menuLi:
                tempStr = htmlDict['treeview'].format(active='', i=i[2], name=i[0], li=''.join(
                    [htmlDict['menuLi'].format(url=appURL + i[3] + getValue + x, text=x) for x in menuLi]))
            else:
                tempStr = htmlDict['li'].format(active='', url=i[3], i=i[2], name=i[0])

        temp.append(tempStr)

    return ''.join(temp)