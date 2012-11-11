# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from EventManager.models import PurplePoster, Movie
from EventManager import rottentomatoes

from datetime import datetime

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
	pp = PurplePoster()
	mv = Movie()
	
	mv.name = request.POST['real-name']
	#mv.PullExternalData(mv.name)
	mv.save()
	
	pp.movie = mv
	pp.alias = request.POST['project-name']
	pp.startTime = datetime.strptime(request.POST['filming-date'], '%m/%d/%Y %H:%M')
	pp.endTime = datetime.strptime(request.POST['filming-date'], '%m/%d/%Y %H:%M')
	pp.submitter = "user name"
	pp.location = request.POST['filming-location']
	pp.locationLat = 0
	pp.locationLon = 0
	pp.save()

	return HttpResponseRedirect("../")
