from rest_framework import serializers

from .models import *


class ConverterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Converter
        fields = ('id', 'file_xml', 'file_xslt', )
