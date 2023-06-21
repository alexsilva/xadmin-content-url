# coding=utf-8
from django.conf import settings

# Models with reverse relationship registration
XD_CONTENT_URL_RELATION_FIELD = getattr(settings, "XD_CONTENT_URL_RELATION_FIELD", 'xd_content_url')
XD_CONTENT_URL_FOR_MODELS = getattr(settings, "XD_CONTENT_URL_FOR_MODELS", [])
