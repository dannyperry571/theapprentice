#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"
import re
import urllib
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult

class cravingsScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='cravings'
		self.name = 'cravings.me'
		self.referrer = 'http://series-cravings.me'
		self.base_url = 'http://series-cravings.me'
		self.timeout = 3
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return results
	
	def process_results(self, html):
		results = []
		pattern = 'src="([^"]+)"\s+frameborder'
		for link in re.finditer(pattern, html, re.DOTALL):
			href = link.group(1)
			host_name = self.get_domain_from_url(href)
			if self.filter_host(host_name):
				url = "%s://%s" % (self.service, href)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				result.quality=QUALITY.HIGH
				results += [result]
		return self.get_response(results)
	

		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			title = args[0].replace(' ', '-').lower()
			title = re.sub("[^a-zA-Z0-9 -]", '', title)
			title = re.sub('^the-', '', title, re.IGNORECASE)
			uri = '/test/%s-season-%s-episode-%s' %  (title, args[1], args[2])
			return uri
		return False
	
