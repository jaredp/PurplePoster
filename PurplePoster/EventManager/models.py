from django.db.models import *

class Project(Model):
	name = CharField(max_length=30)
	company = CharField(blank=True, max_length=30)
	
	def __unicode__(self):
		return self.name

class ProjectAlias(Model):
	alias = CharField(max_length=30)
	project = ForeignKey(Project)
	lastused = DateTimeField()
	
	def __unicode__(self):
		return self.alias + ' :: ' + unicode(self.project)

def getAlias(name, company=None):
	# normalize names
	name = ' '.join(name.split())
	if company: company = ' '.join(company.split())
	
	try:
		return ProjectAlias.objects.get(alias=name, project__company=company)
	except NotFoundError:
		project = Project(name=name, company=company)
		alias = ProjectAlias(alias=name, project=project)
		return alias

class Shoot(Model):
	project = ForeignKey(ProjectAlias)
	poster = FileField(blank=True, upload_to='posters/')
	
	starttime = DateTimeField()
	endtime = DateTimeField()
	
	locationlat = FloatField()
	locationlon = FloatField()
	#locationprecision?



