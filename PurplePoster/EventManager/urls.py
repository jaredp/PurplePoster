from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponseServerError, HttpResponseRedirect
from models import *
from views import *

from datetime import date

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', ListView.as_view(
		template_name='homepage.html',
		queryset=PurplePoster.objects.filter(startTime__gte=date.today()).order_by('-startTime')[:15],
		context_object_name='poster_list',
	)),
	#ex: PurplePoster/homepage.html

	url(r'^poster/(?P<pk>\d+)/$', DetailView.as_view(
		template_name='poster-detail.html',
		model=PurplePoster,
		context_object_name='poster'
	)),
		
	url(r'^submitpurpleposter/$', submitpurpleposter),
	
#	url(r'^user/(?P<pk>\d+)/$', DetailView.as_view(
	
#	url(r'^userpreference/$', ListView.as_view(
#		template_name='user-preference.html',
#		queryset = Movie.objects.all(),
#		context_object_name='movies'
#	)),

	url(r'^user/$', userpreference),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^accounts/profile/$', profile),
	url(r'^trackmovie/$', trackmovie),
	url(r'^trackactor/$', trackactor),
	url(r'^trackposter/$', trackposter),

)
