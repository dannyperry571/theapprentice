import urllib2, urllib
import socket
import json
from urllib2 import URLError, HTTPError
import hashlib
import base64
import traceback
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines import httplib2
from httplib2 import Response

_user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
_accept = 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
_headers = {"User-Agent": _user_agent, "Content-Type": "application/json"}
TMDB_KEY = plugin.get_setting('tmdb_api_key')
TVDB_KEY =  plugin.get_setting('tvdb_api_key')
FANART_KEY =  plugin.get_setting('fanarttv_api_key')
DISABLE_FANART = plugin.get_setting('enable_fanart') == "false"
DISABLE_FANART_SERIES = plugin.get_setting('enable_series_fanart') == "false"
DISABLE_FANART_EPISODES = plugin.get_setting('enable_episode_fanart') == "false"
DISABLE_FANART_MOVIES = plugin.get_setting('enable_movie_fanart') == "false"
DISABLE_FANARTTV = plugin.get_setting('enable_fanarttv') == "false"
DISABLE_TVDB = plugin.get_setting('enable_tvdb') == "false"
DISABLE_TMDB = plugin.get_setting('enable_tmdb') == "false"
DISABLE_TVMAZE = plugin.get_setting('enable_tvmaze') == "false"
DISABLE_OIMDB = plugin.get_setting('enable_oimdbapi') == "false"

def set_art(results, media, url):
	if not results[media]:
		results[media] = url
	return results	

def get_movie_art(imdb_id, tmdb_id=None):
	result = _get_cached_movie(imdb_id)
	if result:
		return result
	result = {"logo": "", "clearlogo": "", "fanart": "", "poster": "", "banner": ""}
	if DISABLE_FANARTTV is False:
		response = search_fanart('movies', imdb_id)
		result = set_art(result, "logo", response["logo"])
		result = set_art(result, "clearlogo", response["clearlogo"])
		result = set_art(result, "banner", response["banner"])
		result = set_art(result, "poster", response["poster"])
		result = set_art(result, "fanart", response["fanart"])
	
	if DISABLE_TMDB is False:
		if not result['fanart'] or not result['poster']:
			response = search_tmdb("movies", tmdb_id)
			result = set_art(result, "fanart", response["fanart"])
			result = set_art(result, "poster", response["poster"])
	
	if DISABLE_OIMDB is False:
		if not result['poster']:
			response = _call_omdbapi('/', params={"r": "json", "i": imdb_id})
			if response and 'Poster' in response:
				result = set_art(result, "poster", [response['Poster'].replace('_V1_SX300', '_V1_SX500')])
	_cache_movie_result(imdb_id, result)
	return result

def get_all_movie_art(imdb_id, tmdb_id):
	results = {"logo": [], "clearlogo": [], "fanart": [], "poster": [], "banner": []}
	if DISABLE_FANARTTV is False:
		try:
			uri = '/movies/%s' % id
			response = _call_fanart(uri)
			if 'hdmovielogo' in response:
				results['logo'] += [art['url'] for art in response['hdmovielogo']]
			if 'hdmovieclearart' in response:
				results['clearlogo'] += [art['url'] for art in response['hdmovieclearart']]
			if 'moviebackground' in response:
				results['fanart'] += [art['url'] for art in response['moviebackground']]
			if 'movieposter' in response:
				results['poster'] += [art['url'] for art in response['movieposter']]
			if 'moviebanner' in response:
				results['banner'] += [art['url'] for art in response['moviebanner']]
		except: pass
	
	if DISABLE_TMDB is False:
		try:
			uri = "/movie/%s/images" % tmdb_id
			response = _call_tmdb(uri)
			if 'backdrops' in response and response['backdrops']:
				results['fanart'] += ["https://image.tmdb.org/t/p/w1280" + art['file_path'] for art in response['backdrops']]
			if 'posters' in response and response['posters']:
				results['poster'] += ["https://image.tmdb.org/t/p/w500" + art['file_path'] for art in response['posters']]
		except: pass
	
	if DISABLE_OIMDB is False:
		try:
			response = _call_omdbapi('/', params={"r": "json", "i": imdb_id})
			if response and 'Poster' in response:
				results['poster'] += [response['Poster'].replace('_V1_SX300', '_V1_SX500')]
		except: pass
	
	return results
	
def get_show_art(tvdb_id, tmdb_id=None, imdb_id=None):
	result = _get_cached_tv(tvdb_id)
	if result:
		return result
	result = {"logo": "", "clearlogo": "", "fanart": "", "poster": "", "banner": ""}
	if DISABLE_FANARTTV is False:
		response = search_fanart('shows', tvdb_id)
		result = set_art(result, "logo", response["logo"])
		result = set_art(result, "clearlogo", response["clearlogo"])
		result = set_art(result, "banner", response["banner"])
		result = set_art(result, "poster", response["poster"])
		result = set_art(result, "fanart", response["fanart"])

	if DISABLE_TVDB is False:
		if not result['fanart'] or not result['poster']:
			response = search_tvdb(tvdb_id)
			result['fanart'] = response['fanart']
			result['poster'] = response['poster']

	if DISABLE_TMDB is False:
		if not result['fanart'] or not result['poster']:
			response = search_tmdb("shows", tmdb_id)
			result = set_art(result, "fanart", response["fanart"])
			result = set_art(result, "poster", response["poster"])
	
	if DISABLE_OIMDB is False and imdb_id is not None:
		if not result['poster']:
			response = _call_omdbapi('/', params={"r": "json", "i": imdb_id})
			if response and 'Poster' in response:
				result = set_art(result, "poster", [response['Poster'].replace('_V1_SX300', '_V1_SX500')])
	_cache_tv_result(tvdb_id, result)
	return result

def get_all_show_art(tvdb_id, tmdb_id=None, imdb_id=None):
	results = {"logo": [], "clearlogo": [], "fanart": [], "poster": [], "banner": []}
	if DISABLE_FANARTTV is False:
		uri = '/tv/%s' % tvdb_id
		try:
			response = _call_fanart(uri)
			if 'hdtvlogo' in response:
				results['logo'] += [art['url'] for art in response['hdtvlogo']]
			if 'clearlogo' in response:
				results['clearlogo'] += [art['url'] for art in response['clearlogo']]
			if 'showbackground' in response:
				results['fanart'] += [art['url'] for art in response['showbackground']]
			if 'tvposter' in response:
				results['poster'] += [art['url'] for art in response['tvposter']]
			if 'tvbanner' in response:
				results['banner'] += [art['url'] for art in response['tvbanner']]
		except: pass
	
	if DISABLE_TVDB is False:
		uri = "/series/%s/images/query" % tvdb_id
		try:
			response = _call_tvdb(uri, params={"keyType": "fanart"})
			results['fanart'] += ["http://thetvdb.com/banners/" + art['fileName'] for art in response['data']]
		except: pass
		try:
			response = _call_tvdb(uri, params={"keyType": "poster"})
			results['poster'] += ["http://thetvdb.com/banners/" + art['fileName'] for art in response['data']]
		except: pass
		
	if DISABLE_TMDB is False:
		uri = '/tv/%s/images' % tmdb_id
		try:
			response = _call_tmdb(uri)
			if 'backdrops' in response and response['backdrops']:
				results['fanart'] += ["https://image.tmdb.org/t/p/w1280" + art['file_path'] for art in response['backdrops']]
			if 'posters' in response and response['posters']:
				results['poster'] += ["https://image.tmdb.org/t/p/w500" + art['file_path'] for art in response['posters']]
		except: pass
	return results

def search_tvdb(tvdb_id):
	result = {"fanart": "", "poster": ""}
	def sort_art(record):
		return record['ratingsInfo']['average']
	uri = "/series/%s/images/query" % tvdb_id
	try:
		response = _call_tvdb(uri, params={"keyType": "fanart"})
		data = sorted(response['data'], reverse=True, key=lambda k: sort_art(k))
		result["fanart"] = "http://thetvdb.com/banners/" + data[0]['fileName']
	except: pass
	try:
		response = _call_tvdb(uri, params={"keyType": "poster"})
		data = sorted(response['data'], reverse=True, key=lambda k: sort_art(k))
		result["poster"] = "http://thetvdb.com/banners/" + data[0]['fileName']
	except: pass

	return result

def search_tmdb(media, tmdb_id):
	result = {"fanart": "", "poster": ""}
	if media == 'shows':
		
		uri = '/tv/%s/images' % tmdb_id
		try:
			response = _call_tmdb(uri)
			if 'backdrops' in response and response['backdrops']:
				result['fanart'] = "https://image.tmdb.org/t/p/w1280%s" % response['backdrops'][0]['file_path']
			if 'posters' in response and response['posters']:
				result['poster'] = "https://image.tmdb.org/t/p/w500%s" % response['posters'][0]['file_path']
		except: pass
	else:
		try:
			uri = "/movie/%s/images" % tmdb_id
			response = _call_tmdb(uri)
			if 'backdrops' in response and response['backdrops']:
				result['fanart'] = "https://image.tmdb.org/t/p/w1280%s" % response['backdrops'][0]['file_path']
			if 'posters' in response and response['posters']:
				result['poster'] = "https://image.tmdb.org/t/p/w500%s" % response['posters'][0]['file_path']
		except: pass
	return result

def search_fanart(media, id):
	result = {"logo": "", "clearlogo": "", "fanart": "", "poster": "", "banner": ""}
	if media == 'shows':
		uri = '/tv/%s' % id
		try:
			response = _call_fanart(uri)
			if 'hdtvlogo' in response:
				result['logo'] = response['hdtvlogo'][0]['url']
			if 'clearlogo' in response:
				result['clearlogo'] = response['clearlogo'][0]['url']
			if 'showbackground' in response:
				result['fanart'] = response['showbackground'][0]['url']
			if 'tvposter' in response:
				result['poster'] = response['tvposter'][0]['url']
			if 'tvbanner' in response:
				result['banner'] = response['tvbanner'][0]['url']
		except: pass
		
	else:
		try:
			uri = '/movies/%s' % id
			response = _call_fanart(uri)
			if 'hdmovielogo' in response:
				result['logo'] = response['hdmovielogo'][0]['url']
			if 'hdmovieclearart' in response:
				result['clearlogo'] = response['hdmovieclearart'][0]['url']
			if 'moviebackground' in response:
				result['fanart'] = response['moviebackground'][0]['url']
			if 'movieposter' in response:
				result['poster'] = response['movieposter'][0]['url']
			if 'moviebanner' in response:
				result['banner'] = response['moviebanner'][0]['url']
		except: pass	
	return result

def get_season_art(tvdb_id, imdb_id=None):
	result = {}
	if DISABLE_TVDB: return result
	
	def sort_art(record):
		return record['ratingsInfo']['average']
	try:
		uri = "/series/%s/images/query" % tvdb_id
		response = _call_tvdb(uri, params={"keyType": "season"})
		data = sorted(response['data'], reverse=False, key=lambda k: sort_art(k))
		for d in data:
			season = int(d["subKey"])
			result[season] = "http://thetvdb.com/banners/" + d["fileName"]
	except: pass
	if DISABLE_TVMAZE is False:
		cache_episode_art(tvdb_id, imdb_id)
	return result

def lookup_tvmaze_id(tvdb_id, imdb_id):
	test = DB.query("SELECT tvmaze_id FROM id_table WHERE tvdb_id=?", [tvdb_id])
	if test:
		return test[0]
	else:
		for id in [tvdb_id, imdb_id]:
			key = "imdb" if id.startswith("tt") else "thetvdb"
			url = "http://api.tvmaze.com/lookup/shows?%s=%s" % (key, id)
			h = httplib2.Http()
			h.follow_redirects = True
			(response, body) = h.request(url)
			if 'content-location' in response:
				redirect = response['content-location']
				tvmaze_id = redirect.split('/')[-1]
				if DB.query("SELECT tvmaze_id FROM id_table WHERE tvdb_id=?", [tvdb_id]):
					DB.execute("UPDATE id_table SET tvmaze_id=? WHERE tvdb_id=?", [tvmaze_id, tvdb_id])
				else:
					DB.execute("INSERT INTO id_table(tvdb_id, tvmaze_id) VALUES(?,?)", [tvdb_id, tvmaze_id])
				DB.commit()
				return tvmaze_id
		return False

def cache_episode_art(tvdb_id, imdb_id=None):
	tvmaze_id = lookup_tvmaze_id(tvdb_id, imdb_id)
	if tvmaze_id:
		uri = "/shows/%s/episodes" % tvmaze_id
		response = _call_tvmaze(uri, params={"specials": 0})
		values = []
		for e in response:
			try:
				values.append([tvdb_id, tvmaze_id, e['season'], e['number'], e['image']['original']])
			except:pass
		if DB.db_type == 'mysql':
			SQL = "INSERT IGNORE INTO tvmaze_episodes(tvdb_id, tvmaze_id, season, episode, screenshot) VALUES(?,?,?,?,?)"
		else:
			SQL = "INSERT INTO tvmaze_episodes(tvdb_id, tvmaze_id, season, episode, screenshot) VALUES(?,?,?,?,?)"
		DB.execute_many(SQL, values)
		DB.commit()

def get_episode_art(tvdb_id, tmdb_id=False, season=False, episode=False, stvdb_id=False):
	result = _get_cached_screenshot(tvdb_id)
	if result:
		return result['screenshot']
	else:
		screenshot = ''
	
	try:
		test = DB.query("SELECT screenshot FROM tvmaze_episodes WHERE tvdb_id=? AND season=? and episode=?", [stvdb_id, season, episode])
		if test:
			screenshot = test[0]
	except: pass
	
		
	if not screenshot:
		try:
			uri = "/tv/%s/season/%s/episode/%s/images" % (tmdb_id, season, episode)
			response = _call_tmdb(uri)
			if response and 'stills' in response and response['stills']:
				screenshot = "https://image.tmdb.org/t/p/w500%s" % response['stills'][0]['file_path']
		except: pass
	
	if not screenshot:
		try:
			uri = '/episodes/%s' % tvdb_id
			response = _call_tvdb(uri)
			if response and 'data' in response and response['data']['filename']:
				screenshot = 'http://thetvdb.com/banners/_cache/' + response['data']['filename']
		except: pass
	
	if screenshot:
		_cache_screenshot(tvdb_id, screenshot)
	return screenshot
	
def _get_cached_tv(tvdb_id):
	return DB.query_assoc("SELECT logo, clearlogo, fanart, poster, banner FROM fanart_shows WHERE tvdb_id=?", [tvdb_id])
	
def _get_cached_movie(imdb_id):
	return DB.query_assoc("SELECT logo, clearlogo, fanart, poster, banner FROM fanart_movies WHERE imdb_id=?", [imdb_id])

def _get_cached_screenshot(tvdb_id):
	return DB.query_assoc("SELECT screenshot FROM fanart_episodes WHERE tvdb_id=?", [tvdb_id])

def _cache_tv_result(tvdb_id, result):
	SQL = "INSERT INTO fanart_shows(tvdb_id, logo, clearlogo, fanart, poster, banner) VALUES(?,?,?,?,?,?)"
	DB.execute(SQL, [tvdb_id, result['logo'], result['clearlogo'], result['fanart'], result['poster'], result['banner']])
	DB.commit()

def _cache_movie_result(imdb_id, result):
	SQL = "INSERT INTO fanart_movies(imdb_id, logo, clearlogo, fanart, poster, banner) VALUES(?,?,?,?,?,?)"
	DB.execute(SQL, [imdb_id, result['logo'], result['clearlogo'], result['fanart'], result['poster'], result['banner']])
	DB.commit()

def _cache_screenshot(tvdb_id, screenshot):
	DB.execute("INSERT INTO fanart_episodes(tvdb_id, screenshot) VALUES(?,?)", [tvdb_id, screenshot])
	DB.commit()

def _call_fanart(uri, params=None, data=None, cache_limit=False, timeout=None, method=None):
	_base_url = "http://webservice.fanart.tv/v3"
	_headers = {"User-Agent": _user_agent, "api-key": FANART_KEY}
	timeout = timeout if timeout is not None else 5
	json_data = json.dumps(data) if data else None

	url = '%s%s' % (_base_url, uri)
	if params is not None:
		url += '?' + urllib.urlencode(params)
	while True:	
		try:
			request = urllib2.Request(url, data=json_data, headers=_headers)
			if method is not None:
				request.get_method = lambda: method.upper()
			f = urllib2.urlopen(request, timeout=timeout)
			result = f.read()
			response = json.loads(result)
			break
		except HTTPError as e:
			plugin.log(e, url)
			return False
		except URLError as e:
			plugin.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
		except socket.timeout as e:
			plugin.log("%s %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
	return response


def tvdb_login():
	token = plugin.get_property("tvdb_token")
	if not token:
		uri = '/login'
		data = {"apikey": TVDB_KEY}
		response = _call_tvdb(uri, data=data, auth=False)
		token = response['token']
		plugin.set_property("tvdb_token", token)
	return token	

def _call_tvdb(uri, params=None, data=None, timeout=None, method=None, auth=True):
	_base_url = "https://api.thetvdb.com"
	timeout = timeout if timeout is not None else 5
	json_data = json.dumps(data) if data else None
	auth_trial = 0
	url = '%s%s' % (_base_url, uri)
	if params is not None:
		url += '?' + urllib.urlencode(params)	
	if auth:
		token = tvdb_login()
		_headers["Authorization"] = "Bearer %s" % token
	
	while True:	
		try:
			request = urllib2.Request(url, data=json_data, headers=_headers)
			if method is not None:
				request.get_method = lambda: method.upper()
			f = urllib2.urlopen(request, timeout=timeout)
			result = f.read()
			response = json.loads(result)
			break
		except HTTPError as e:
			plugin.log(e.code)
			if e.code == 401 and auth_trial == 0:
				plugin.clear_property("tvdb_token")
				auth_trial = 1
			else:
				plugin.log(e, url)
				return False
		except URLError as e:
			plugin.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
		except socket.timeout as e:
			plugin.log("%s %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
	return response
	
def _call_tmdb(uri, params={"api_key": TMDB_KEY}, data=None, cache_limit=False, timeout=None, method=None):

	_base_url = "https://api.themoviedb.org/3"
	timeout = timeout if timeout is not None else 5
	json_data = json.dumps(data) if data else None

	url = '%s%s' % (_base_url, uri)
	if params is not None:
		url += '?' + urllib.urlencode(params)
	
	while True:	
		try:
			request = urllib2.Request(url, data=json_data, headers=_headers)
			if method is not None:
				request.get_method = lambda: method.upper()
			f = urllib2.urlopen(request, timeout=timeout)
			result = f.read()
			response = json.loads(result)
			break
		except HTTPError as e:
			plugin.log(e, url)
			return False
		except URLError as e:
			plugin.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
		except socket.timeout as e:
			plugin.log("%s %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
	return response	


def _call_omdbapi(uri, params=None, data=None, cache_limit=False, timeout=None, method=None):

	_base_url = "http://www.omdbapi.com"
	timeout = timeout if timeout is not None else 5
	json_data = json.dumps(data) if data else None

	url = '%s%s' % (_base_url, uri)
	if params is not None:
		url += '?' + urllib.urlencode(params)

	while True:	
		try:
			request = urllib2.Request(url, data=json_data, headers=_headers)
			if method is not None:
				request.get_method = lambda: method.upper()
			f = urllib2.urlopen(request, timeout=timeout)
			result = f.read()
			response = json.loads(result)
			break
		except HTTPError as e:
			plugin.log(e, url)
			return False
		except URLError as e:
			plugin.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
		except socket.timeout as e:
			plugin.log("%s %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
	return response	

def _call_tvmaze(uri, params=None, data=None, cache_limit=False, timeout=None, method=None):

	_base_url = "http://api.tvmaze.com"
	timeout = timeout if timeout is not None else 5
	json_data = json.dumps(data) if data else None

	url = '%s%s' % (_base_url, uri)
	if params is not None:
		url += '?' + urllib.urlencode(params)
	
	while True:	
		try:
			request = urllib2.Request(url, data=json_data, headers=_headers)
			if method is not None:
				request.get_method = lambda: method.upper()
			f = urllib2.urlopen(request, timeout=timeout)
			result = f.read()
			response = json.loads(result)
			break
		except HTTPError as e:
			plugin.log(e, url)
			return False
		except URLError as e:
			plugin.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
		except socket.timeout as e:
			plugin.log("%s %s" % (e,url), LOG_LEVEL.VERBOSE)
			return False
	return response	
	
	