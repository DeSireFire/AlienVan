from django.shortcuts import render

# Create your views here.
def index(request):
    '''
    响应首页
    :param request:
    :return:
    '''
    context = {
        'title': '次元圣经',
        'novelTypes_html':[],
        'novelTypes':[],
    }

    return render(request,'index/index.html',context)