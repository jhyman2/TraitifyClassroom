from django.conf.urls import patterns, include, url
import views
from tests.admin import admin_site
urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin_site.urls)),
    url(r'^tests/', include('tests.urls', namespace='tests')),
    url(r'^$', views.home),
)
