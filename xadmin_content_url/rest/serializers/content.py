# coding=utf-8
from rest_framework import serializers
from django.utils import html


class GenericContentUrlSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(source="pk")
	title = serializers.SerializerMethodField('get_title')
	url = serializers.SerializerMethodField("get_absolute_url", read_only=True)

	def get_absolute_url(self, instance):
		return instance.get_absolute_url()

	def get_title(self, instance):
		# handle xss
		return html.escape(str(instance))

	class Meta:
		fields = ('id', 'title', 'url')
