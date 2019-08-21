from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^vuePage/getAllEvent', views.getPageEvent, name='getPageEvent'),
    url(r'^vuePage/$', views.vuePage, name='vuePage'),
    url(r'^homePage/$', views.homePage, name='homePage'),
    url(r'^homePage2/$', views.homePage2, name='homePage2'),
    url(r'^homePage2/getAllCamera$', views.getAllCamera),
    url(r'^eventReport/$', views.eventReport, name='eventReport'),
    url(r'^eventReport/getPageEvent$', views.getPageEvent),
    url(r'^eventReport/getDataToExport$', views.getDataToExport),
    url(r'^$', views.index, name='index'),
]
