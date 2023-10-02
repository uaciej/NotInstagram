from rest_framework import serializers
from .models import Image

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['file', 'expiration_time']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file', 'uploaded_at']