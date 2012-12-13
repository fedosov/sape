# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.core.mail import mail_admins

from sape.sape_client import sape_manager


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            sape_manager.update_cache()

        except Exception, e:
            print e
            raise
            mail_admins("Sape error", unicode(e))
