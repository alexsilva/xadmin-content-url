from xadmin.sites import site, register
from xadmin.views import ModelAdminView
from xadmin.views.edit import ModelFormAdminView
from xadmin_content_url.models import XdSiteViewUrl
from xadmin_content_url.views import ContentUrlAdminView
from xadmin_content_url.xplugin import XdContentUrlAdminPlugin, XdContentUrlAdminRestPlugin

site.register_plugin(XdContentUrlAdminPlugin, ModelFormAdminView)
site.register_plugin(XdContentUrlAdminRestPlugin, ModelAdminView)

site.register_view("^xd-content-url/", ContentUrlAdminView, 'xd_content_url')


@register(XdSiteViewUrl)
class XdSiteViewOptions:
	xd_content_url_enable = True
	xd_content_search_fields = ('name',)
	hidden_menu = True

