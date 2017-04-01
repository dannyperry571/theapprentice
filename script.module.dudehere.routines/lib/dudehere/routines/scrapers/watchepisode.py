'''
watchepisode.tv source plugin
@natko1412, 2015

'''

import re
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult


class watchepisodeScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='watchepisode'
		self.name = 'watchepisode.tv'
		self.referrer = 'http://www.watchepisodes1.com'
		self.base_url = 'http://www.watchepisodes1.com'
		self.get_debrid_hosts()

	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		url = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		html = self.request(url, append_base=False, cache=30)
		if html:
			results = self.process_results(html)
		return self.get_response(results)
	

	def process_results(self, html):
		results = []
		pattern = 'data-actuallink="([^"]+)" data-hostname="([^"]+)"'
		for match in re.finditer(pattern, html, re.DOTALL):
			url, host_name = match.groups()
			if self.filter_host(host_name):
				url = "%s://%s" % (self.service, url)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				results += [result]
		return results
		
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = self.url_friendly(args[0])
			uri = "/%s" % showname
			html = self.request(uri, cache=86640)
			season = str(args[1]).zfill(2)
			episode = str(args[2]).zfill(2)
			pattern = 's%se%s" href="([^"]+)"' % (season, episode)
			match = re.search(pattern, html, re.DOTALL)
			if match:
				href = match.group(1)
				return href