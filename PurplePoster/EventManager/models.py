from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import rottentomatoes, re


# Used by the Movie class
class Actor(models.Model):
	actorRot_ID = models.CharField(max_length=20)
	firstName = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	def __unicode__(self):
		return self.firstName + ' ' + self.lastName

# Used by the Movie class
class Producer(models.Model):
	producerRot_ID = models.CharField( max_length=20)
	producerName = models.CharField(max_length=100)
	def __unicode__(self):
		return self.producerName

# Used by the Movie class
class Poster(models.Model):
	posterURL = models.URLField();			#Consider changing this to FileField instead
	def __unicode__(self):
		return self.posterURL


# Used by PurplePoster class
class Image(models.Model):
	imageURL = models.URLField();			#Consider changing this to FileField instead
	def __unicode__(self):
		return self.imageURL

class Location(models.Model):
	lat = models.FloatField(blank=True,null=True)
	lon = models.FloatField(blank=True,null=True)
	def __unicode__(self):
		return self.id

###########################################################################
######					Main Class Models  								###
###########################################################################

class Movie(models.Model):
	movieRot_ID = models.CharField(blank=True, null=True, max_length=20)
	name = models.CharField(max_length=100)
	actor = models.ManyToManyField(Actor)
	producer = models.ManyToManyField(Producer)
	summary = models.CharField(blank=True, null=True, max_length=1000)
	poster = models.ManyToManyField(Poster)
	releaseDate = models.DateField(blank=True, null=True)
	#movie.merge method, which needs to combine duplicates (models.py)
	#TODO: This should be fixed now, no need for the merge method, please confirm
	def __unicode__(self):
		return self.name
	def PullExternalData(self, movie_name):
		rotMovie = rottentomatoes.SearchMovie(movie_name)[0]
		try:
			return Movie.objects.get(movieRot_ID = rotMovie['id'])
		except ObjectDoesNotExist:
			self.movieRot_ID = rotMovie['id']
			self.name = rotMovie['title']

			for e in rotMovie['abridged_cast']:
				a = Actor(actorRot_ID = e['id'], firstName = re.search('\w+',e['name']).group(0).strip() , lastName = re.search('\w+$',e['name']).group(0).strip())
				a.save()
				self.actor.add(a)
			#TODO external data node missing
			#self.producer = rotMovie['abridged_directors']
			self.summary = rotMovie['synopsis']
			for desc in rotMovie['posters']:
				p = Poster(posterURL = rotMovie['posters'][desc])
				p.save()
				self.poster.add(p)
			self.releaseDate = rotMovie['release_dates']['theater']
			self.save()
			return self

	def GetRawData(self, movie_name):
		return rottentomatoes.SearchMovie(movie_name)[0]


class PurplePoster(models.Model):
	alias = models.CharField(max_length = 100) 
	movie = models.ForeignKey(Movie)
	submitter = models.CharField(max_length=100)    #edit later to point to user intsance
	startTime = models.DateField()
	endTime = models.DateField(blank=True, null=True)
	location = models.CharField(max_length=100)
	locationLat = models.FloatField(blank=True,null=True)
	locationLon = models.FloatField(blank=True,null=True)
	image = models.ManyToManyField(Image)
	#Comments: Comment[]
	#submitImage()  
	def __unicode__(self):
		return self.alias + ' :: ' + unicode(self.movie)

	def getMovieInfo(self):
		return Movie.objects.get(id=self.movie.id)

	def SetGeoLocation(self, location):
		getLoc = rottentomatoes.GetLocationCoordinates(location)[0]
		self.LocationLat = getLoc['lat']
		self.LocationLat = getLoc['lng']
		self.save()

class UserPreference(models.Model):
	user = models.OneToOneField(User)
	movie = models.ManyToManyField(Movie)
	actor = models.ManyToManyField(Actor)
	#producer = models.ManyToManyField(Producer)
	purplePoster = models.ManyToManyField(PurplePoster)
	area = models.ManyToManyField(Location)

