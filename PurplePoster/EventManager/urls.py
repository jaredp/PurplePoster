from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from models import *
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$',TemplateView.as_view(template_name='homepage.html')),
	#ex: PurplePoster/homepage.html

	url(r'^(?P<alias>\d+)/$', purpleposterpage, name='purpleposterpage'),
	# ex: /PurplePoster/alias/
	
)
