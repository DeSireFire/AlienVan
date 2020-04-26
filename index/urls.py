from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('file', views.fileShow),
    path('pans', views.index),
]
