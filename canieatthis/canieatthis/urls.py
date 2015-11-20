"""canieatthis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from website import views

urlpatterns = [
    url(r'^$', 'website.views.home', name='home'),

    # API-related URLs

    # view all approved foods
    url(r'^api/food_list/$', views.FoodList.as_view(), name='food_list'),
    # view all unapproved (user-submitted) foods
    url(r'^api/user_list/$', views.UserList.as_view(), name='user_list'),
    # add user-submitted foods
    url(r'api/add_food/$', views.AddFood.as_view(), name='add_food'),

]
