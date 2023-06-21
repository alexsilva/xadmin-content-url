from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from xadmin_content_url.forms import fields
from xadmin_content_url.models import XdContentUrl, XdUrl


class XdContentUrlField(GenericRelation):
	description = "Field that allows selecting url for generic content."

	def __init__(self, to=None, **kwargs):
		super().__init__(to or XdContentUrl, **kwargs)
		self.editable = True

	def xd_save_form_data(self, instance, object_id, content_type: ContentType):
		url = XdUrl.objects.get_or_create(
			content_type=content_type,
			object_id=object_id,
		)[0]
		obj = self.remote_field.model.objects.get_or_create(
			content_type=ContentType.objects.get_for_model(instance),
			object_id=instance.pk,
			url=url
		)[0]
		return obj

	def save_form_data(self, instance, data: list):
		"""data: [(object_id, content_type),...]"""
		if not data:
			return
		objs = []
		for item in data:
			obj = self.xd_save_form_data(instance, *item)
			objs.append(obj.pk)
			break
		self.remote_field.model.objects.exclude(pk__in=objs).delete()

	def value_from_object(self, obj):
		"""Return the value of this field in the given model instance."""
		return super().value_from_object(obj).all()

	def formfield(self, **kwargs):
		defaults = {
			'form_class': fields.XdContentUrlField
		}
		defaults.update(kwargs)
		return super().formfield(**defaults)
