import django.forms as django_forms
from xadmin.util import vendor
from xadmin.views import BaseAdminPlugin
from xadmin_content_url.serializers.content import GenericContentUrlSerializer


class XdContentUrlAdminPlugin(BaseAdminPlugin):

	def init_request(self, *args, **kwargs):
		return True

	def get_media(self, media):
		media += vendor("datatables.css", "datatables.js")
		media += django_forms.Media(js=[
			"xd_content_url/js/xd_sel_url.js"
		])
		return media


class XdContentUrlAdminRestPlugin(BaseAdminPlugin):
	xd_content_url_serializer = GenericContentUrlSerializer
	xd_content_url_rest_param = "xd_ct_url"

	def init_request(self, *args, **kwargs):
		return bool(self.request.GET.get('plugin') == self.xd_content_url_rest_param)

	def get_serializer_class(self, __):
		serializer_class = self.xd_content_url_serializer
		meta = serializer_class.Meta
		serializer_class = type(serializer_class.__name__,  (serializer_class,), {
			'Meta': type("Meta", (meta, ), {'model': self.model})
		})
		return serializer_class
