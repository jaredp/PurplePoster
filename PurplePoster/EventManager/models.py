from django.db import models


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
	def __unicode__(self):
		return self.name



class PurplePoster(models.Model):
	alias = models.CharField(max_length = 100) 
	movie = models.ForeignKey(Movie)
	submitter = models.CharField(max_length=100)    #edit later to point to user intsance
	startTime = models.DateTimeField()
	endTime = models.DateTimeField(blank=True, null=True)
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
	

