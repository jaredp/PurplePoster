from django.db import connection

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
	for row in cursor.fetchall():
		print row
