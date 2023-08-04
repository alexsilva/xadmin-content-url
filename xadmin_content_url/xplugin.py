import django.forms as django_forms
from django.core.exceptions import PermissionDenied
from xadmin.util import vendor
from xadmin.views import BaseAdminPlugin
from xadmin_content_url.filters import SearchFilterBackend
from xadmin_content_url.rest.permissions import HasContentUrlPermission
from xadmin_content_url.rest.serializers.content import GenericContentUrlSerializer


class XdContentUrlAdminPlugin(BaseAdminPlugin):

	def init_request(self, *args, **kwargs):
		return True

	def get_media(self, media):
		media += vendor("datatables.css", "datatables.js", "xadmin.bs.modal.js")
		media += django_forms.Media(js=[
			"xd_content_url/js/xd_sel_url.js"
		], css={
			'screen': ('xd_content_url/css/xd_sel_url.css',)
		})
		return media


class XdContentUrlAdminRestPlugin(BaseAdminPlugin):
	xd_content_url_serializer = GenericContentUrlSerializer
	xd_content_url_search_filter = SearchFilterBackend
	xd_content_urls_permissions = [HasContentUrlPermission]
	xd_content_url_rest_param = "xd_ct_url"
	xd_content_url_enable = True

	def init_request(self, *args, **kwargs):
		is_active = bool(self.xd_content_url_enable and self.request.GET.get('plugin') == self.xd_content_url_rest_param)
		# The plugin is read-only because the permissions have been rewritten.
		if is_active and self.admin_view.request_method not in ['get', 'options', 'head']:
			raise PermissionDenied('read only')
		return is_active

	def get_permissions(self, __):
		"""Validates only list permissions"""
		return [permission() for permission in self.xd_content_urls_permissions]

	def get_serializer_class(self, __):
		serializer_class = self.xd_content_url_serializer
		meta = serializer_class.Meta
		serializer_class = type(serializer_class.__name__,  (serializer_class,), {
			'Meta': type("Meta", (meta, ), {'model': self.model})
		})
		return serializer_class

	def filter_queryset(self, queryset, *args, **kwargs):
		search_filter_backend = self.xd_content_url_search_filter()
		queryset = search_filter_backend.filter_queryset(
			self.admin_view.request, queryset,
			self.admin_view
		)
		return queryset
