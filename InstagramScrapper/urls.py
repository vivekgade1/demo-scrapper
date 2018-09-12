"""InstagramScrapper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.views import serve
from django.urls import path
from django.views.generic import RedirectView

from InstaVision import views

urlpatterns = [
    url(r'^$', serve, kwargs={'path': 'client/index.html'}),
    url(r'^getInstaVisionData', views.get_insta_data),
    url(r'^getAuthToken', views.get_auth_token, name='get_auth_token'),
    url(r'^getImageContent', views.get_images_file),
    url(r'^getComments', views.get_comments_file),
    url(r'^getAllRequests', views.get_all_requests),

    url(r'^(?!/?static/client/)(?!/?media/)(?P<path>.*\..*)$',
    RedirectView.as_view(url='/static/client/%(path)s', permanent=False)),
    url(r'^(?P<path>.*)/$', serve, kwargs={'path': 'client/index.html'})
]
urlpatterns += staticfiles_urlpatterns()
