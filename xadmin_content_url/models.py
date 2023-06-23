from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class XdUrl(models.Model):
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	content_object = GenericForeignKey("content_type", "object_id")

	def _get_object_url(self):
		# noinspection PyBroadException
		try:
			obj = self.content_object
		except Exception as exc:
			url = None
		else:
			url = obj and obj.get_absolute_url()
		return url or ''

	def __str__(self):
		return self._get_object_url()

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

	url = models.ForeignKey(XdUrl, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.url)

	class Meta:
		indexes = [
			models.Index(fields=["content_type", "object_id"]),
		]
