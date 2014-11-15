from django.conf.urls import patterns, include, url
#from tests import views

urlpatterns = patterns('tests',
	url(r'log/$', 'views.log', name='log'),
	url(r'assess/$', 'views.testDetail', name='test_detail'),
	url(r'assess/result/$', 'views.testResult', name='test_result'),
)
