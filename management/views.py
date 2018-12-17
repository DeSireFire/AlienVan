from django.shortcuts import render

# Create your views here.
def index(request):
    '''
    响应首页
    :param request:
    :return:
    '''
    context = {
        'title': '主页',
    }

    return render(request, 'index/index.html', context)