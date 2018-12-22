from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from odTools import authentication


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
        'title': '管理页',
    }
    init_type = request.GET.get('odType')
    auth_url = authentication.getClient(init_type)

    print(auth_url)
    # context['auth_url'] = auth_url
    return render(request, 'index/index.html', context)

def callBackBinding(request):
    import json
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
        return HttpResponse(json.dumps(json_data), content_type="application/json")

    else:
        return HttpResponse('It is not a POST request!!!')

import asyncio

@asyncio.coroutine
def run_gets(client):
    coroutines = [client.drive('me').request().get_async() for i in range(3)]
    for future in asyncio.as_completed(coroutines):
        drive = yield from future
        print(drive.id)

