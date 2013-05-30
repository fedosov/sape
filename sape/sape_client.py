# -*- coding: utf-8 -*-

import os
import pickle
import re
import logging
import urllib

from django.conf import settings

SAPE_URL = "http://dispenser-01.sape.ru/code.php?user=%(user_id)s&host=%(host)s&charset=%(charset)s&as_txt=true"
CACHE_LIFETIME = 3600


class SapeFetchError(Exception):
	pass


class SapeClient(object):
	cache = None
	cache_time = None

	def __init__(self):
		self.init_log()
		self.get_links_from_cache()

	def get_links_from_cache(self):
		filename = self.get_cache_file()
		self.cache = {}

		try:
			self.log.info('Load links from file "%s"', filename)
			self.log.info('Cache time %s, file time %s, id %s', self.cache_time, os.path.getmtime(filename), id(self))
			data = open(filename, 'rb').read()
			cache = pickle.loads(data)
			self.cache = cache
			self.cache_time = os.path.getmtime(filename)

		except (EOFError, IOError, OSError):
			self.log.debug('Cache file "%s" not found', filename)

	def init_log(self):
		self.log = logging.getLogger('sape')
		self.log.setLevel(getattr(settings, 'LOG_LEVEL', logging.ERROR))
		handler = logging.FileHandler(getattr(settings, 'SAPE_LOG', '/dev/null'))
		LOG_FORMAT = u'%(levelname)s %(asctime)s: %(message)s'
		LOG_TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
		handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT))
		self.log.addHandler(handler)

	def get_links(self, uri):
		if self.need_to_refresh():
			self.get_links_from_cache()

		if uri in self.cache:
			return self.cache[uri]
		else:
			return self.cache.get('__sape_new_url__', [])

	def need_to_refresh(self):
		filename = self.get_cache_file()

		if not os.path.exists(filename):
			self.log.error('Cache file "%s" not found', filename)
			return False

		if not os.path.getsize(filename):
			self.log.error('Cache file "%s" is empty', filename)
			return False

		if os.path.getmtime(filename) > self.cache_time:
			self.log.info('Fresh cache file "%s" found', filename)
			return True

		return False

	def update_cache(self):
		self.log.info("Update cache for host %s: start", settings.SAPE_DOMAIN)
		try:
			links = self.fetch_links()
			links_dict = self.parse_data(links)
			self.save_links(links_dict)
			self.log.info("Update cache for host %s: finish", settings.SAPE_DOMAIN)
		except (IOError, UnicodeDecodeError), e:
			message = "Cannot update cache file: %s (url %s)" % (e, self.sape_url())
			self.log.error(message)
			raise SapeFetchError(message)

	def fetch_links(self):
		return urllib.urlopen(self.sape_url()).read()

	def sape_url(self):
		return SAPE_URL % {'user_id': settings.SAPE_USER, 'host': settings.SAPE_DOMAIN, 'charset': settings.SAPE_CHARSET}

	def parse_data(self, data):
		"""
		Parse raw data retrieved from sape server.
		"""
		db = {}
		data = data.decode(settings.SAPE_CHARSET)
		data = data.split('\n', 2)

		if data[0].startswith('FATAL ERROR'):
			raise SapeFetchError(data[0])

		db['__sape_delimiter__'] = data[1]

		for block in data[2].split('\n'):
			slices = block.split('||SAPE||')
			db[slices[0]] = slices[1:]

		return db

	def save_links(self, links_dict):
		data = pickle.dumps(links_dict)

		filename = self.get_cache_file()

		try:
			os.makedirs(os.path.dirname(filename))
		except OSError:
			# директория для кеша уже существует
			pass

		open(filename, 'wb').write(data)

	def get_cache_file(self):
		prefix = re.sub(r'(?i)[^-a-z0-9]', '_', settings.SAPE_DOMAIN)
		return '%s/%s.links.db' % (os.path.dirname(settings.SAPE_DIR), prefix)


sape_manager = SapeClient()
