# coding=utf-8
from rest_framework import serializers


class GenericContentUrlSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(source="pk")
	title = serializers.CharField(source='__str__')
	url = serializers.SerializerMethodField("get_absolute_url", read_only=True)

	def get_absolute_url(self, instance):
		return instance.get_absolute_url()

	class Meta:
		fields = ('id', 'title', 'url')
