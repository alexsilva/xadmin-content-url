import django.forms as django_forms
from xadmin.views import BaseAdminPlugin


class XdContentUrlAdminPlugin(BaseAdminPlugin):

	def init_request(self, *args, **kwargs):
		return True

	def get_media(self, media):
		media += django_forms.Media(js=[
			"xd_content_url/js/xd_sel_url.js"
		])
		return media
