# -*- coding: utf-8 -*-

# import logging
# import mechanize
#
# from django.conf import settings
# from django.core.management.base import NoArgsCommand
# from django.core.mail import mail_admins
#
#
# class Command(NoArgsCommand):
#     def init_log(self):
#         self.log = logging.getLogger('sape')
#         self.log.setLevel(settings.LOG_LEVEL)
#         handler = logging.FileHandler(settings.SAPE_LOG)
#         LOG_FORMAT = u'%(levelname)s %(asctime)s: %(message)s'
#         LOG_TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
#         handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT))
#         self.log.addHandler(handler)
#
#     def handle_noargs(self, **options):
#         self.init_log()
#
#         self.log.info("Checking for errors")
#
#         br = mechanize.Browser()
#         br.open("https://www.sape.ru/")
#         br.select_form(nr=0)
#         br['username'] = settings.SAPE_USERNAME
#         br['password'] = settings.SAPE_PASSWORD
#
#         br.submit()
#
#         response = br.open("https://www.sape.ru/site_links.php?site_id=%s&filter[status]=error" % settings.SAPE_SITE_ID)
#         html = response.read()
#
#         if u"Ссылок не найдено".encode('cp1251') in html:
#             self.log.info('no errors')
#         else:
#             self.log.error('Error links were found')
#             mail_admins("Sape error", "There are bad links in your site %s" % settings.SAPE_SITE_ID)
