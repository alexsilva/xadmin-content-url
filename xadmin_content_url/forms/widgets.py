from django.forms import TextInput


class XdContentUrlInput(TextInput):
	base_template_name = "django/forms/widgets/text.html"
	template_name = "xd_content_url/forms/widgets/url.html"

	@staticmethod
	def simple_model_format(qs):
		items = [f"{o.content_type.app_label}:{o.content_type.model}:{o.object_id}"
		         for o in qs]
		return ','.join(items)

	@staticmethod
	def simple_model_string(qs):
		items = [str(o) for o in qs]
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
