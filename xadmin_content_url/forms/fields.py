import django.forms as django_forms
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from xadmin_content_url.forms import widgets
from xadmin_content_url.models import XdUrl


class XdContentUrlField(django_forms.Field):
	widget = widgets.XdContentUrlInput
	widget_model = XdUrl

	def __init__(self, *args, empty_value=None, **kwargs):
		super().__init__(*args, **kwargs)
		if empty_value is None:
			self.empty_value = []

	def prepare_value(self, value):
		if value in self.empty_values or isinstance(value, list):
			return value
		else:
			return self.to_python(value)

	def to_python(self, value):
		if value in self.empty_values:
			return self.empty_value
		items = []
		for index, item in enumerate(value.split(',')):
			app_label, model_name, object_id = item.split(":")
			model = apps.get_model(app_label, model_name)
			object_id = model._meta.pk.to_python(object_id)
			ctype = ContentType.objects.get_for_model(model)
			items.append(self.widget_model(object_id=object_id, content_type=ctype))
		return items
