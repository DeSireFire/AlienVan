from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from odTools import authentication
# Create your views here.
def home(request):
    # context = initialize_context(request)
    context = {}

    return render(request, 'home.html', context)


def initBinding(request):
    context = {}
    init_type = request.GET.get('odType')
    auth_url = authentication.getClient(init_type)
    context['auth_url'] = auth_url
    return render(request, 'home.html', context)

def callBackBinding(request):
    import json
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
        return HttpResponse(json.dumps(json_data), content_type="application/json")

    else:
        return HttpResponse('It is not a POST request!!!')

