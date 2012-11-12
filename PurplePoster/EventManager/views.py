# Create your views here.2
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from EventManager.models import PurplePoster, Movie
from EventManager import rottentomatoes

from datetime import datetime
import time
import parsedatetime as pdtlib
import logging
pdtlib.log.setLevel(logging.ERROR)

def parse_date(dtstring):
	#unclear if calendars are reusable
	cal = pdtlib.Calendar()
	d, rettype = cal.parse(dtstring)
	
	# awful kludge, see parsedatetime.Calendar.parse
	if rettype == 0:
		return None
	elif rettype == 1:
		return datetime.fromtimestamp(mktime(d))
	elif rettype == 2:
		return None
	elif rettype == 3:
		return d

def homepage(request):
    latest_posters_list = PurplePoster.objects.order_by('startTime')[:5]
    template = loader.get_template('EventManager/index.html')
    context = Context({
        'latest_posters_list': latest_posters_list,
    })
    return HttpResponse(template.render(context))

def purpleposterpage(request, PurplePoster):
    return HttpResponse("You're looking at the PurplePoster %s." % PurplePoster.alias + "<->" + PurplePoster.movie)

def submitpurpleposter(request):
	
	# I think the duplicate movie scenario is now handled in models.py
	# it aint pretty tho!!!
	mv = Movie()
	if request.POST['real-name'] and request.POST['real-name'] != '':
		mv.name = request.POST['real-name']
	else:
		mv.name = request.POST['project-name']

	mv = mv.PullExternalData(mv.name)	
	mv.save()
	
	pp = PurplePoster()
	pp.movie = mv
	pp.alias = request.POST['project-name']
	
	filmingdate = parse_date(request.POST['filming-date'])
	pp.startTime = pp.endTime = time.strftime("%Y-%m-%d %H:%M:%S", filmingdate)
	
	pp.submitter = "user name"	#FIXME
	
	#pp.locationLat = float(request.POST['location-lat'])
	#pp.locationLon = float(request.POST['location-lon'])

	if request.POST['filming-location'] != '':
		pp.location = request.POST['filming-location']
		latlng = rottentomatoes.GetLocationCoordinates(pp.location)
		pp.locationLat = float(latlng['lat'])
		pp.locationLon = float(latlng['lng'])

	pp.save()

	return HttpResponseRedirect('/poster/%s/' % pp.pk)
