__author__ = 'rvidal'
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^logout_nuevo/$', views.logout_view, name='logout' ),
)