from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^jadonsa', views.Jadonsa.as_view(), name='jadonsa'),
	url(r'^test', views.test, name='test'),
]
