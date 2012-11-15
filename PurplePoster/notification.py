#!/usr/bin/python

from PurplePoster import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.db import connection
from EventManager.models import *

class EmailAlert(object):
	def __init__(self, userid, email):
		self.userid = userid
		self.email = email
		
		self.movieAlerts = []
		self.posterAlerts = []
		self.locationAlerts = []
		self.actorAlerts = []

def getNotifications():
	cursor = connection.cursor()
	cursor.execute('''
		SELECT
	   		UA.userpreference_id userPreferenceID, 
	  		A.actorName EntityName, P.id PosterID, 'A' flag
		FROM        EventManager_userpreference_actor UA
		INNER JOIN  EventManager_actor A
		ON          A.id = UA.actor_ID
		INNER JOIN  EventManager_movie_actor MA
		ON          MA.actor_id = UA.actor_ID
		INNER JOIN  EventManager_movie M
		ON          M.id = MA.movie_ID 
		INNER JOIN  EventManager_purpleposter P
		ON          M.id = P.movie_ID
		WHERE       P.startTime = CURDATE() + 1
		UNION
		SELECT      UM.userpreference_id, M.name, P.id, 'M' flag
		FROM        EventManager_userpreference_movie UM
		INNER JOIN  EventManager_movie M
		ON          M.id = UM.movie_ID
		INNER JOIN  EventManager_purpleposter P
		ON          M.id = P.movie_ID
		WHERE       P.startTime = CURDATE() + 1
		UNION
		SELECT      UP.userpreference_id, P.alias, P.id, 'P' flag
		FROM        EventManager_userpreference_purplePoster UP
		INNER JOIN  EventManager_purpleposter P
		ON          P.id = UP.purpleposter_ID
		WHERE       P.startTime = CURDATE() + 1
		UNION
		SELECT      UA.userpreference_id, '', P.id, 'L' flag
		FROM        EventManager_userpreference_area UA
		INNER JOIN  EventManager_location L
		ON          UA.location_id = L.id
		INNER JOIN  EventManager_purpleposter P
		ON          P.Locationlat >= L.lat - 0.07 AND L.lat + 0.07
		AND         P.Locationlon BETWEEN L.lon - 0.07 AND L.lon + 0.07
		WHERE       P.startTime = CURDATE() + 1
	''')
	
	alertsByUser = {}
	for (prefid, alertname, posterid, flag) in cursor.fetchall():
		user = UserPreference.objects.get(pk=prefid).user
		userid = user.pk
		
		if userid not in alertsByUser:
			user
			alertsByUser[userid] = EmailAlert(userid, user.email)
		email = alertsByUser[userid]
		
		alertSets = {
			'A': email.actorAlerts,
			'M': email.movieAlerts,
			'L': email.locationAlerts,
			'P': email.posterAlerts
		}
		
		notification = (posterid, alertname)
		alertSets[flag].append(notification)
		
	return alertsByUser
			
print getNotifications()
