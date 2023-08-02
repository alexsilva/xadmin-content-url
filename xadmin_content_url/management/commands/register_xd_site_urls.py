import sys

from django.core.management import BaseCommand
from xadmin_content_url.models import XdSiteViewUrl
from xadmin_content_url.settings import XD_CONTENT_URL_FOR_VIEW_NAME, XD_CONTENT_URL_VIEW_NAME_AUTO_REMOVE


class Command(BaseCommand):
	help = """Register urls from XdSiteViewUrl model"""

	site_view_name_setting = XD_CONTENT_URL_FOR_VIEW_NAME
	site_view_auto_remove_setting = XD_CONTENT_URL_VIEW_NAME_AUTO_REMOVE
	site_view_name_model = XdSiteViewUrl

	def remove_unregistered(self):
		removed = set(self.site_view_name_model.objects.values_list('ref', flat=True)) - set(self.site_view_name_setting)
		if removed:
			qs = self.site_view_name_model.objects.filter(ref__in=list(removed))
			qs.delete()
		return removed

	def handle(self, *args, **options):
		for ref in self.site_view_name_setting:
			item = self.site_view_name_setting[ref]
			print(f"Registry {item['name']}", file=sys.stdout)
			defaults = {
				'name': item['name'],
				'view_name': item['view_name']
			}
			obj, created = self.site_view_name_model.objects.get_or_create(ref=ref, defaults=defaults)
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

		if self.site_view_auto_remove_setting:
			removed = self.remove_unregistered()
			print(f"Removed {len(removed)} objs...")
