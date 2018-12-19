from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.graph_helper import get_user, get_calendar_events
# Create your views here.
def home(request):
  # context = initialize_context(request)
  context = {}

  return render(request, 'home.html', context)

