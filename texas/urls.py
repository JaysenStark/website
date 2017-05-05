
from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = 'texas'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^action/$', views.action, name='action'),
    url(r'^start/$', views.start, name='start'),
    url(r'^update/$', views.update, name='update'),
    url(r'^test/$', views.test, name='test'),
    url(r'^logout/$', views.logout, name='logout'),
]
