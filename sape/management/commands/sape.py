# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand


class Command(BaseCommand):

	def handle(self, *args, **options):
		if "fetch" in args:
			from ...sape_client import sape_manager
			sape_manager.update_cache()
