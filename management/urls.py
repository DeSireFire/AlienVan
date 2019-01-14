from django.urls import path,re_path
from . import views

app_name = 'management'
urlpatterns = [
    path('',views.panAction),
    path('pans',views.pans),
    path('file',views.fileShow),
    # path('',views.test),
    path('addpan',views.addPan),
    path('del',views.fileDel),
    path('rename',views.fileRename),
    # path('signin', views.sign_in, name='signin'),
]
