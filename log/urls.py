from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^vuePage/getAllEvent', views.getPageEvent, name='getPageEvent'),
    url(r'^vuePage/$', views.vuePage, name='vuePage'),
    # url(r'^homePage/$', views.homePageBak, name='homePage'),
    url(r'^homePage/$', views.homePage, name='homePage'),
    url(r'^homePage/getAllCamera$', views.getAllCamera),
    url(r'^homePage/getAllEventByCamera$', views.getAllEventByCamera),
    url(r'^eventReport/$', views.eventReport, name='eventReport'),
    url(r'^eventReport/getPageEvent$', views.getPageEvent),
    url(r'^eventReport/getDataToExport$', views.getDataToExport),
    url(r'^$', views.index, name='index'),
]
