import django.forms as django_forms
from django.utils.translation import gettext_lazy as _
from xadmin.sites import site
from xadmin.widgets import AdminSelectWidget


def get_models_registry(admin_site=None):
	if admin_site is None:
		admin_site = site
	for model, admin in admin_site._registry.items():
		if getattr(admin, 'xd_content_url_enable', False):
			yield model, admin


def _get_models_choices(admin_site=None):
	items = []
	for model, admin in get_models_registry(admin_site=admin_site):
		opts = model._meta
		items.append((opts.label_lower, opts.verbose_name))
	return items


class ContentUrlForm(django_forms.Form):
	content = django_forms.ChoiceField(label=_("Content"), widget=AdminSelectWidget)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		field = self.fields.get('content')
		if field:
			field.choices =_get_models_choices()
