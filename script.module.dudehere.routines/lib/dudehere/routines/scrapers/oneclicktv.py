#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"
import re
import urllib
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult


class oneclicktvScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='oneclicktv'
		self.name = 'oneclicktvshows.com'
		self.referrer = 'http://oneclicktvshows.com'
		self.base_url = 'http://oneclicktvshows.com'
		self.timeout = 3
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html, str(args['season']).zfill(2), str(args['episode']).zfill(2))
		return results
	
	def process_results(self, html, season, episode):
		results = []
		pattern = '\.S%sE%s\.' % (season, episode)
		show = re.compile(pattern)
		pattern = '<a\s+style="color:\s+#008000;"\s+href="([^"]+)"\s+target="_blank">([^ ]+) &#8211; ([^<]+)</a>'
		for link in re.finditer(pattern, html, re.DOTALL):
			href, file, size = link.groups()
			if show.search(file):
				host_name = self.get_domain_from_url(href)
				if self.filter_host(host_name):
					url = "%s://%s" % (self.service, href)
					result = ScraperResult(self.debrid_hosts, self.service, host_name, url, file)
					result.quality=self.test_quality(file)
					if size.endswith('MB'):
						size = float(size[0:len(size)-3])
						size = size * 1024 * 1024
					else:
						size = float(size[0:len(size)-3])
						size = 100 * 1024 * 1024 * 1024
					result.size = size
					if file.endswith('.mkv'):
						result.extension = 'mkv'
					if file.endswith('.mpv'):
						result.extension = 'mp4'	
					results += [result]

		return self.get_response(results)
	

		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			title = args[0].replace(' ', '-').lower()
			title = re.sub("[^a-zA-Z0-9 -]", '', title)
			uri = '/%s/' %  (title)
			return uri
		return False
	
