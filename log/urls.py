from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^layui/$', views.layui, name='layui'),
    url(r'^layui/getUser$', views.getUser),
    url(r'^$', views.index, name='index'),
]