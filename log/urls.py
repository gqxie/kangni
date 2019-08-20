from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^vuePage/getAllEvent', views.getPageEvent, name='getPageEvent'),
    url(r'^vuePage/$', views.vuePage, name='vuePage'),
    url(r'^homePage/$', views.homePage, name='homePage'),
    url(r'^eventReport/$', views.eventReport, name='eventReport'),
    url(r'^eventReport/getUser$', views.getUser),
    url(r'^eventReport/getPageEvent$', views.getPageEvent),
    url(r'^$', views.index, name='index'),
]
