from django.apps import apps
from django.contrib.contenttypes.models import ContentType
import django.forms as django_forms
from xadmin_content_url.forms import widgets


class XdContentUrlField(django_forms.Field):
	widget = widgets.XdContentUrlInput

	def __init__(self, *args, empty_value='', **kwargs):
		super().__init__(*args, **kwargs)
		self.empty_value = empty_value

	def to_python(self, value):
		if value in self.empty_values:
			return self.empty_value
		items = []
		for index, item in enumerate(value.split(',')):
			app_label, model_name, object_id = item.split(":")
			model = apps.get_model(app_label, model_name)
			object_id = model._meta.pk.to_python(object_id)
			ctype = ContentType.objects.get_for_model(model)
			items.append((object_id, ctype))
		return items
