from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class CardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Card
        fields = ('id', 'user', 'name', 'owner', 'pan', 'balance', 'expired_date')


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    card_name = serializers.StringRelatedField(
        many=False,
        source='card',
        read_only=True,
    )

    class Meta:
        model = Transaction
        fields = ('id', 'card', 'card_name', 'operation_type', 'operation_type', 'sum', 'date', 'contr_agent', 'user')
