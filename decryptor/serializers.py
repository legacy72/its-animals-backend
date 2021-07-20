from rest_framework import serializers
from .models import MD5Rainbow


class MD5RainbowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MD5Rainbow
        fields = ('id', 'hash_value', 'key')