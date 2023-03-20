from rest_framework import serializers

from posts.models import Post, PostTag


class PostTagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    slug = serializers.CharField(max_length=50)

    class Meta:
        model = PostTag

