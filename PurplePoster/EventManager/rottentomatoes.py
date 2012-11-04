import urllib, json, pprint
API_KEY = "apikey=yx4uxh5f7zvcxtfst6xrxw3u"
BASE_URL = "http://api.rottentomatoes.com/api/public/v1.0/movies.json"


def PullExternalData(movie_name):
	return SearchMovie(movie_name)[0]

def SearchMovie(movie_name, page_limit=1, page_num=1):
	url = BASE_URL + '?'
	url = url + 'q=' + str(movie_name) + '&'
	url = url + 'page_limit=' + str(page_limit) + '&'
	url = url + 'page=' + str(page_num) + '&'
	url = url + API_KEY

	movies = json.load(urllib.urlopen(url))['movies']
	#pprint.pprint(movies)
	return movies
