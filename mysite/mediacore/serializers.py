from rest_framework import serializers
from .models import ImageFile, VideoFile


class ImageFileSerializer(serializers.ModelSerializer):
    file = serializers.CharField(source='file.url')

    class Meta:
        model = ImageFile
        fields = ('id', 'file',)


class VideoFileSerializer(serializers.ModelSerializer):
    file = serializers.CharField(source='file.url')

    class Meta:
        model = VideoFile
        fields = ('id', 'file',)