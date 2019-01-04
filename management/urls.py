from django.urls import path,re_path
from . import views

app_name = 'management'
urlpatterns = [
    path('',views.panAction),
    re_path(r'pans/(.*?).html$',views.pans),
    # path('',views.test),
    path('addpan/',views.addPan),
    path('nd/',views.initBinding),
    path('cetest/',views.ce_test),
    path('odtest/',views.od_ce_test),
    path('codecallback/',views.callBackBinding),
    # path('signin', views.sign_in, name='signin'),
]
