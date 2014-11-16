from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
#from tests import urls

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^tests/', include('tests.urls', namespace='tests')),
	url(r'^', views.home),
)
