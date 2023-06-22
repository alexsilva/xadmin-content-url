import rest_framework_datatables.filters
import rest_framework_datatables.pagination
import rest_framework_datatables.renderers

from rest_framework.settings import api_settings
from xadmin import sites
from xadmin.sites import site
from xadmin.views import ModelAdminView
from xadmin.views.edit import ModelFormAdminView
from xadmin_content_url.views import ContentUrlAdminView
from xadmin_content_url.xplugin import XdContentUrlAdminPlugin, XdContentUrlAdminRestPlugin

site.register_plugin(XdContentUrlAdminPlugin, ModelFormAdminView)
site.register_plugin(XdContentUrlAdminRestPlugin, ModelAdminView)

site.register_view("^xd-content-url/", ContentUrlAdminView, 'xd_content_url')


@sites.register(ModelAdminView)
class ModelAdminViewRestOptions:

	def __init__(self, *args, **kwargs):
		kwargs['pagination_class'] = rest_framework_datatables.pagination.DatatablesPageNumberPagination
		renderer_classes = kwargs.setdefault('renderer_classes', list(api_settings.DEFAULT_RENDERER_CLASSES))
		renderer = rest_framework_datatables.renderers.DatatablesRenderer
		if renderer not in renderer_classes:
			renderer_classes.append(renderer)
		filter_backends = kwargs.setdefault('filter_backends', [])
		backend = rest_framework_datatables.filters.DatatablesFilterBackend
		if backend not in filter_backends:
			filter_backends.append(backend)
		super().__init__(*args, **kwargs)
		