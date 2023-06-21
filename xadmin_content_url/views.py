from crispy_forms.helper import FormHelper
from django.shortcuts import render
from xadmin.views import BaseAdminView
from xadmin_content_url.forms.content import ContentUrlForm


class ContentUrlAdminView(BaseAdminView):
	form_class = ContentUrlForm

	def get_helper(self):
		helper = FormHelper()
		helper.form_tag = False
		helper.form_class = 'form-horizontal'
		helper.field_class = 'col-sm-8'
		helper.use_custom_control = False
		helper.include_media = False
		return helper

	def get(self, request, **kwargs):
		helper = self.get_helper()
		form = self.form_class()
		form.helper = helper
		context = {
			'form': form
		}
		return render(request, template_name="xd_content_url/forms/model_form.html",
		              context=context)
