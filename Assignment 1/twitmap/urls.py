
from django.conf.urls import url, include
from django.contrib import admin
from twitmap import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^tweet/', views.home, name='home'),
	
]