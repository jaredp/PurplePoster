# Create your views here.2
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext, loader
from django.shortcuts import render_to_response
from django.views.generic import DetailView, ListView, TemplateView
from EventManager.models import *
from EventManager import rottentomatoes
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
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

def submitpurpleposter(request):
	# I think the duplicate movie scenario is now handled in models.py
	# it aint pretty tho!!!
	try:
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
		
	except Exception as e:
		return HttpResponseRedirect('/error/')

class ErrorView(TemplateView):
	def get_context_data(self):
		return RequestContext(self.request)

	def profile(request):
		return HttpResponseRedirect('/')

class SearchPosters(ListView):
	def get_query(self):
		return self.request.GET['search-string']
	
	def get_queryset(self):
		searchstring = self.get_query()

		from django.db.models import Q
		posters = PurplePoster.objects.filter(Q(alias__contains=searchstring) 
			| Q(movie__name__contains = searchstring) 
			| Q(movie__actor__actorName__contains = searchstring))
		#FIXIT: Eliminate Duplicates from result list

		return posters

class UserPreferenceView(TemplateView):
	def get_context_data(self):
		up = getUserPreference(self.request.user)
		user_movies = up.movie.all
		user_actors = up.actor.all
		user_posters = up.purplePoster.all
		return RequestContext(self.request, {
        	'movies': Movie.objects.all,
       		'actors': Actor.objects.all,
        	'posters': PurplePoster.objects.all,
        	'user': self.request.user,
        	'user_movies': user_movies,
        	'user_actors': user_actors,
			'user_posters': user_posters,
		})


def profile(request):
	return HttpResponseRedirect('/user/')

#def trackmovie(request):
#	up = UserPreference()
#	usernm = request.POST['user-name']
#	movieid = request.POST['movie-id']
#	
#	if(usernm!=''):
#		userobj = User.objects.get(username = usernm)					#Get numeric user ID from User
#		movieobj = Movie.objects.get(id = movieid)
#		
#		print "Tracking Movie:", movieobj, " for User:" , userobj, " having user ID:", userobj.id
#
#		up = UserPreference(UserPreference.objects.get(user = userobj.id))		#Use numeric ID to find user's preference records
#		if(up != None):
#			print "User Preference record located:", up.user, " ...using..."
#		else:															#create new record if it does not exist
#			print "User has not past preference records, saving user's preference entry now..."
#		up.user = userobj
#		up.save()														#save new record
#		up = up.movie.add(movieobj)										#Add movie to User Preference record
#		up.save()														#Save record
#	return HttpResponseRedirect('/user/')
def trackmovie(request):
	up = getUserPreference(request.user)
	up.addUserMovie(request.POST['movie-id'])
	return HttpResponseRedirect('../')

def trackactor(request):
	up = getUserPreference(request.user)
	up.addUserActor(request.POST['actor-id'])
	return HttpResponseRedirect('../')

def trackposter(request):
	up = getUserPreference(request.user)
	up.addUserPoster(request.POST['poster-id'])
	return HttpResponseRedirect('../')

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			message = None
			form.save()

			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			user = authenticate(username=username, password=password)
			request.user = user
			login(request, user)
			return HttpResponseRedirect('../')

	else:
		form = UserCreationForm()
	return render_to_response('signup.html', {'form': form, }, context_instance=RequestContext(request))
