from xadmin.views import BaseAdminPlugin


class XdContentUrlAdminPlugin(BaseAdminPlugin):
	xd_content_url = False

	def init_request(self, *args, **kwargs):
		return bool(self.xd_content_url)
