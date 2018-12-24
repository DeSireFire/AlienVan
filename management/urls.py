from django.urls import path
from . import views


urlpatterns = [
    path('',views.home),
    path('nd/',views.initBinding),
    path('cetest/',views.ce_test),
    path('odtest/',views.od_ce_test),
    # path('signin', views.sign_in, name='signin'),
]
