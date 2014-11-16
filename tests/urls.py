from django.conf.urls import patterns, url

from views import LogView, TestDetailView, GenerateView

urlpatterns = patterns('',
	url(r'log/$', LogView.as_view(), name='log'),
	url(r'assess/$', TestDetailView.as_view(), name='test_detail'),
	url(r'generate/(?P<user_count>\d+)/$', GenerateView.as_view(), name='generate'),
)
