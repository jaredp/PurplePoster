# Create your views here.2
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from EventManager.models import PurplePoster, Movie, Actor, User, UserPreference
from EventManager import rottentomatoes

from datetime import datetime
from time import mktime, strftime
import parsedatetime as pdtlib
import logging
pdtlib.log.setLevel(logging.ERROR)

def parse_date(dtstring):
	#this doesn't work for some obvious ones... we may want to consider replacing it
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

#def homepage(request):
#   latest_posters_list = PurplePoster.objects.order_by('startTime')[:5]
#    template = loader.get_template('EventManager/homepage.html')
#    context = Context({
#        'latest_posters_list': latest_posters_list,
#    })
#    return HttpResponse(template.render(context))

def purpleposterpage(request, PurplePoster):
    return HttpResponse("You're looking at the PurplePoster %s." % PurplePoster.alias + "<->" + PurplePoster.movie)

def submitpurpleposter(request):
	
	# I think the duplicate movie scenario is now handled in models.py
	# it aint pretty tho!!!
	mv = Movie()
	if request.POST['real-name'] != '':
		mv.name = request.POST['real-name']
	else:
		mv.name = request.POST['project-name']
	
	try:
		mv = mv.PullExternalData(mv.name)
	except:
		pass
	mv.save()
	
	pp = PurplePoster()
	pp.movie = mv
	pp.alias = request.POST['project-name']
	# TODO: add production company name
	
	filmingdate = parse_date(request.POST['filming-date'])
	pp.startTime = pp.endTime = filmingdate
	
	pp.submitter = "user name"	#FIXME
	
	if request.POST['filming-location'] != '':
		pp.location = request.POST['filming-location']
		latlng = rottentomatoes.GetLocationCoordinates(pp.location)
		pp.locationLat = float(latlng['lat'])
		pp.locationLon = float(latlng['lng'])
	else:
		pp.locationLat = request.POST['location-lat']
		pp.locationLon = request.POST['location-lon']
		# if this fails, reject and require a filming-location, gracefully

	pp.save()

	return HttpResponseRedirect('/poster/%s/' % pp.pk)


def searchposters(request):
	searchstring = request.POST['search-string']
	print "Search String is:", searchstring
	if(searchstring!=''):
		#Search Poster Name for searchstring
		qualifying_posters_list = PurplePoster.objects.filter(alias__contains=searchstring)
		
		#Search Film Name for searchstring
		all_posters = PurplePoster.objects.all()
		for poster in all_posters:
			print "MOVIE ID being searched:", poster.movie
			postermovie = Movie.objects.filter(name = poster.movie)[0]
			if (searchstring in postermovie.name):
				#TODO: Eliminate duplicates or append only if not previously appended
				len(qualifying_posters_list) #or anything that will evaluate and hit the db
				qualifying_posters_list._result_cache.append(poster) #Append poster to QuerySet

		print "List of search results:", qualifying_posters_list
		template = loader.get_template('searchresultspage.html')
		context = Context({'qualifying_posters_list': qualifying_posters_list,})
		return HttpResponse(template.render(context))


def userpreference(request):
	context = Context({
        'movies': Movie.objects.all,
        'actors': Actor.objects.all,
        'posters': PurplePoster.objects.all,
        'user' :request.user,
	})
	context.update(csrf(request))
	return render_to_response("userpreference.html", context)

def profile(request):
	return HttpResponseRedirect('/user/')

def trackmovie(request):
	up = UserPreference()
	usernm = request.POST['user-name']
	movieid = request.POST['movie-id']
	print "Tracking Movie:", movieid, " for User:" , usernm
	if(usernm!=''):
		userobj = User.objects.get(username = usernm)					#Get numeric user ID from User
		print userobj
		uplist = UserPreference.objects.filter(user = userobj.id)		#Use numeric ID to find user's preference records
		if(uplist.__len__()==1):
			up = uplist[0]			#retrieve user's User Preference record
		else:						#create new record if it does not exist
			up.user = userobj
			up.save()					#save new record
		up = up.movie.add(movieid)		#Add movie to User Preference record
		up.save()						#Save record
	return HttpResponseRedirect('/user/')

def trackactor(request):
	up = UserPreference()
	up = up.addMUserActor(request.POST['actor'])
	return HttpResponseRedirect('/user/')
def trackposter(request):
	up = UserPreference()
	up = up.addMUserPoster(request.POST['poster'])
	return HttpResponseRedirect('/user/')
