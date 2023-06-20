from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class XdUrl(models.Model):
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	content_object = GenericForeignKey("content_type", "object_id")

	def __str__(self):
		return self.content_object.get_absolute_url()

	class Meta:
		indexes = [
			models.Index(fields=["content_type", "object_id"]),
		]


class XdContentUrl(models.Model):
	created_at = models.DateTimeField(_("created at"), auto_now_add=True)
	updated_at = models.DateTimeField(_("updated at"), auto_now=True)

	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	content_object = GenericForeignKey("content_type", "object_id")

	url = models.OneToOneField(XdUrl, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.url)

	class Meta:
		indexes = [
			models.Index(fields=["content_type", "object_id"]),
		]
