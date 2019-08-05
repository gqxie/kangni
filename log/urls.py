from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^layui/$', views.layui, name='layui'),
    url(r'^$', views.index, name='index'),
]