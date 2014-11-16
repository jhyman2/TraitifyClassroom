from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from tests.admin import MyAdminSite

urlpatterns = patterns('',
	url(r'^admin/', include(MyAdminSite.urls)),
	url(r'^tests/', include('tests.urls', namespace='tests')),
	url(r'^', views.home),
)
