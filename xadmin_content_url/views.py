from django.shortcuts import render
from xadmin.views import BaseAdminView
from xadmin_content_url.forms.content import ContentUrlForm


class ContentUrlAdminView(BaseAdminView):
	form_class = ContentUrlForm

	def get(self, request, **kwargs):
		context = {
			'form': self.form_class()
		}
		return render(request, template_name="xd_content_url/forms/model_form.html",
		              context=context)
