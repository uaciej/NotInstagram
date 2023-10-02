from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Tier, Account

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ['id', 'name', 'thumbnail_sizes', 'link_enabled', 'expiring_link_enabled']

class AccountSerializer(serializers.ModelSerializer):
    tier = TierSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'email', 'created_at', 'tier', 'is_staff', 'is_active']


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect email or password.')
        attrs['user'] = user
        return attrs