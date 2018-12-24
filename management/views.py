from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home(request):
    # context = initialize_context(request)
    context = {
        'title':'管理页',
    }

    return render(request, 'management/index.html', context)

def initBinding(request):
    '''

    :param odType: onedrive 类型 普通版或者商业版
    :return:
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

# @csrf_exempt
def callBackBinding(request):
    print(request.body)
    print(request.method)
    print(request.POST.get('code'))
    import json
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
        return HttpResponse(json.dumps(json_data), content_type="application/json")

    else:
        return HttpResponse('It is not a POST request!!!')


def ce_test(request):
    x = request.GET.get('x', '1')
    y = request.GET.get('y', '1')
    from .tasks import test
    a = test.delay(x,y).get()
    print('這裡是:'+a)
    res = {'code': 200, 'message': 'ok', 'data': [{'x': x, 'y': y}]}
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
