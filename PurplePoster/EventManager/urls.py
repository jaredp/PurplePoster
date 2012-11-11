from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from models import *
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', ListView.as_view(
		template_name='homepage.html',
		queryset=PurplePoster.objects.order_by('startTime')[:5],
		context_object_name='poster_list',
	)),
	#ex: PurplePoster/homepage.html

	url(r'^poster/(?P<pk>\d+)/$', DetailView.as_view(
		template_name='poster-detail.html',
		model=PurplePoster,
		context_object_name='poster'
	)),
	# ex: /PurplePoster/alias/
	
	url(r'^summarymap$', ListView.as_view(
		template_name='summarymap.html',
		queryset=PurplePoster.objects.order_by('startTime')[:5],
		context_object_name='summary_list',
	)),

)
