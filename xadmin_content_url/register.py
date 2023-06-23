# coding=utf-8
import warnings
from django.utils.translation import ugettext_lazy as _
from django.apps import apps
from xadmin_content_url import settings
from xadmin_content_url.db.fields import XdContentUrlField
from xadmin_content_url.models import XdContentUrl


def register_models(*models):
	"""Registers models that receive urls"""
	for model in models:
		try:
			app_label, model_name = model.split(".", 1)
		except ValueError as exc:
			warnings.warn(f"invalid model '{model}', expected 'app_label.model_name'",
			              RuntimeWarning)
			continue
		# with the reverse relationship it is possible to create xd content in the generic model
		model = apps.get_model(app_label, model_name)
		field = XdContentUrlField(XdContentUrl, verbose_name=_("Content URL"))
		field.contribute_to_class(model, settings.XD_CONTENT_URL_RELATION_FIELD)
