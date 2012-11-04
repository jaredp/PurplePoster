from django.db import models


class Movie(models.Model):
	name = models.CharField(max_length=40)
	#Actors: String[]
	#Producers: String[]
	summary = models.CharField(blank=True, max_length=300)
	#Posters: URL[]
	#Trailers: URL[]
	releaseDate = models.DateTimeField(blank=True)
	#movie.merge method, which needs to combine duplicates (models.py)
	def __unicode__(self):
		return self.name



class PurplePoster(models.Model):
	alias = models.CharField(blank=False, max_length = 50)
	movie = models.ForeignKey(Movie)
	submitter = models.CharField(max_length=50)    #edit later to point to user intsance
	startTime = models.DateTimeField(blank=False)
	endTime = models.DateTimeField(blank=True)
	location = models.CharField(blank=False, max_length=100)
	locationLat = models.FloatField(blank=True)
	locationLon = models.FloatField(blank=True)
	#Image: Image[]
	#Comments: Comment[]
	#submitImage()
	#GetMovieInfo(Movie movie)
	def __unicode__(self):
		return self.alias + ' :: ' + unicode(self.movie)

	def getMovieInfo():


#def getAlias(name, company=None):
	# normalize names
#	name = ' '.join(name.split())
#	if company: company = ' '.join(company.split())
	
#	try:
#		return ProjectAlias.objects.get(alias=name, project__company=company)
#	except NotFoundError:
#		project = Project(name=name, company=company)
#		alias = ProjectAlias(alias=name, project=project)
#		return alias

#class Shoot(Model):
#	poster = FileField(blank=True, upload_to='posters/')

