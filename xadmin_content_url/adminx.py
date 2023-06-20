from xadmin.sites import site
from xadmin.views.edit import ModelFormAdminView
from xadmin_content_url.xplugin import XdContentUrlAdminPlugin

site.register_plugin(XdContentUrlAdminPlugin, ModelFormAdminView)
