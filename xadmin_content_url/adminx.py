from xadmin.sites import site
from xadmin.views.edit import ModelFormAdminView
from xadmin_content_url.views import ContentUrlAdminView
from xadmin_content_url.xplugin import XdContentUrlAdminPlugin

site.register_plugin(XdContentUrlAdminPlugin, ModelFormAdminView)
site.register_view("^xd-content-url/", ContentUrlAdminView, 'xd_content_url')
