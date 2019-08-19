from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^vuePage/getAllEvent', views.getAllEvent, name='getAllEvent'),
    url(r'^vuePage/$', views.vuePage, name='vuePage'),
    url(r'^homePage/$', views.homePage, name='homePage'),
    url(r'^layui/$', views.layui, name='layui'),
    url(r'^layui/getUser$', views.getUser),
    url(r'^layui/getAllEvent$', views.getAllEvent),
    url(r'^$', views.index, name='index'),
]
