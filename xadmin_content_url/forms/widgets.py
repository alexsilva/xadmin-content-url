from django.forms import TextInput
from xadmin_content_url.models import XdUrl


class XdContentUrlInput(TextInput):
	base_template_name = "django/forms/widgets/text.html"
	template_name = "xd_content_url/forms/widgets/url.html"

	@staticmethod
	def simple_model_format(data: list[XdUrl]):
		items = []
		if not data:
			return ''
		for url in data:
			items.append(f"{url.content_type.app_label}:{url.content_type.model}:{url.object_id}")
		return ','.join(items)

	@staticmethod
	def simple_model_string(data: list[XdUrl]):
		if not data:
			return ''
		items = [str(o) for o in data]
		return ','.join(items)

	def get_context(self, name, value, attrs):
		context = super().get_context(name, self.simple_model_format(value), attrs)
		widget = context['widget']
		widget['base_template_name'] = self.base_template_name
		widget['type'] = 'hidden'
		widget['is_hidden'] = True
		widget['sel'] = {
			'type': self.input_type,
			'value': self.simple_model_string(value)
		}
		return context
