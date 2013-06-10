from django import template
from django.conf import settings

from sape.sape_client import sape_manager

register = template.Library()

SAPE_DOMAIN = getattr(settings, 'SAPE_DOMAIN', None)
SAPE_USER = getattr(settings, 'SAPE_USER', 'foobar')
SAPE_DIR = getattr(settings, 'SAPE_DIR', '.')


@register.simple_tag
def sape_links(request):
	query_string = request.META.get('QUERY_STRING', '')

	uri = u''.join([request.META["PATH_INFO"],
	               len(query_string) and '?' or '',
	               query_string])

	links = sape_manager.get_links(uri)
	return u" ".join(links)
