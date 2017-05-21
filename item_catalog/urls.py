"""repository URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name = "Home"),
    url(r'^additem/$', views.additem),
    url(r'^edititem/$', views.edititem),
    url(r'^fbconnect', views.fbconnect),
    url(r'^catalog.json$', views.jsonprint, name = "jsonprint"),
    url(r'^catalog/(?P<category>[a-zA-Z]+)/items$', views.categoryitems),
    url(r'^catalog/(?P<category>[a-zA-Z]+)/(?P<item>[a-zA-Z]+)$', views.viewitem, {'function': 'view'}),
    url(r'^catalog/(?P<category>[a-zA-Z]+)/(?P<item>[a-zA-Z]+)/edit$', views.viewitem, {'function': 'edit'}),
    url(r'^catalog/(?P<category>[a-zA-Z]+)/(?P<item>[a-zA-Z]+)/editsubmit$', views.edititem),
    url(r'^catalog/(?P<category>[a-zA-Z]+)/(?P<item>[a-zA-Z]+)/delete/yes$', views.deleteitemconfirm, name = "deleteitemconfirm"),
    url(r'^catalog/(?P<category>[a-zA-Z]+)/(?P<item>[a-zA-Z]+)/delete$', views.deleteitem, name = "deleteitem"),
    url(r'^logout/$', views.logout, name = "logout"),
    url(r'^register/$', views.register, name = "register"),
    url(r'^catalogview/$', views.login),
    url(r'^signin/$', views.signin, name = "signin"),



]
