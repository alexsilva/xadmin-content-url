from django.conf import settings
from django.contrib.auth import get_permission_codename
from rest_framework import permissions


class HasContentUrlPermission(permissions.BasePermission):
	"""Validates the permission list given in 'XD_CONTENT_URL_PERMISSIONS'"""
	message = 'has content url permission.'

	def has_object_permission(self, request, view, obj):
		# Permission name to validate when accessing rest api data.
		urls_permissions = getattr(settings, "XD_CONTENT_URL_PERMISSIONS", ())
		has_perm, opts = True, view.opts
		for name in urls_permissions:
			code_name = get_permission_codename(name, opts)
			has_perm &= request.user.has_perm(f"{opts.app_label}.{code_name}", obj=obj)
		return has_perm

	def has_permission(self, request, view):
		return self.has_object_permission(request, view, None)
