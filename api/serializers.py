from rest_framework import serializers

from utils import to_hash
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = serializers.ModelSerializer.to_representation(self, instance)
        del result['login']
        del result['password']
        return result

    def create(self, validated_data):
        password = validated_data['password']
        validated_data['password'] = to_hash(password)
        return serializers.ModelSerializer.create(self, validated_data)

    def update(self, instance, validated_data):
        return serializers.ModelSerializer.update(self, instance, validated_data)

    class Meta:
        model = Account
        fields = '__all__'
