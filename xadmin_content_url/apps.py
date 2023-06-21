# coding=utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class XdContentUrlConfig(AppConfig):
	"""Config xadmin_content_url"""
	name = 'xadmin_content_url'
	verbose_name = _("Content Url")

	def ready(self):
		from xadmin_content_url import settings as xd_settings
		from xadmin_content_url.register import register_models
		register_models(*xd_settings.XD_CONTENT_URL_FOR_MODELS)
