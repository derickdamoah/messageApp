from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import include, url

urlpatterns = [
    path('', views.home, name="home"),
    path('message', views.message, name="message"),
    path('sendMessage', views.sendMessage, name="sendMessage"),
    path('reply', views.reply, name='reply'),
    url(r'^sms/$', views.sms_response),
]