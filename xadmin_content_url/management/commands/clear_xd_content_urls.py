import sys

from django.core.management import BaseCommand
from xadmin_content_url import settings as xd_settings
from xadmin_content_url.models import XdContentUrl


class Command(BaseCommand):
	help = """Removes instances of content that is no longer registered."""
	xd_content_url_model = XdContentUrl

	def handle(self, *args, **options):
		url_for_models = [m.lower() for m in xd_settings.XD_CONTENT_URL_FOR_MODELS]

		for instance in self.xd_content_url_model.objects.all():
			try:
				if model_class := instance.content_type.model_class():
					label_lower = model_class._meta.label_lower
				else:
					label_lower = None
			except Exception as exc:
				label_lower = None

			if label_lower is None or label_lower not in url_for_models:
				print(f"Remove [{label_lower}] {instance}", file=sys.stdout)
				instance.delete()
				instance.url.delete()
