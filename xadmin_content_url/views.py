from crispy_forms.helper import FormHelper
from django.shortcuts import render
from xadmin.util import xstatic
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

	def get_context(self):
		ctx = super().get_context()
		ctx['dt_language_url'] = xstatic("datatables.lang")[0]
		return ctx

	def get(self, request, **kwargs):
		helper = self.get_helper()
		form = self.form_class(prefix='xdm')
		form.helper = helper
		context = self.get_context()
		context.update(
			form=form
		)
		return render(request, template_name="xd_content_url/forms/model_form.html",
		              context=context)
