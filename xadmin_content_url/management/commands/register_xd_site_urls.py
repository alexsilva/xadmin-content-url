import sys

from django.core.management import BaseCommand
from xadmin_content_url.models import XdSiteViewUrl
from xadmin_content_url.settings import XD_CONTENT_URL_FOR_VIEW_NAME


class Command(BaseCommand):
	help = """Register urls from XdSiteViewUrl model"""

	def handle(self, *args, **options):
		for ref in XD_CONTENT_URL_FOR_VIEW_NAME:
			item = XD_CONTENT_URL_FOR_VIEW_NAME[ref]
			print(f"Registry {item['name']}", file=sys.stdout)
			defaults = {
				'name': item['name'],
				'view_name': item['view_name']
			}
			obj, created = XdSiteViewUrl.objects.get_or_create(ref=ref, defaults=defaults)
			update_count = 0
			if not created:
				updated = False
				for key in defaults:
					value = defaults[key]
					if not updated and getattr(obj, key) != value:
						updated = True
					setattr(obj, key, value)
				if updated:
					update_count += 1
					obj.save()
			if update_count > 0:
				print(f"Updated {update_count} objs...", file=sys.stdout)
