from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^addEvent$', views.addEvent),
]