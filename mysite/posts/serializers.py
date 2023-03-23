from rest_framework import serializers
from posts.models import Post, PostTag
from mediacore.models import ImageFile
from mediacore.serializers import ImageFileSerializer, VideoFileSerializer


class PostTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    slug = serializers.CharField(max_length=50)

    class Meta:
        model = PostTag
        fields = ('name', 'slug',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    pub_date = serializers.CharField()
    only_for_adult = serializers.BooleanField()
    for_autenticated_users = serializers.BooleanField()
    disable_comments = serializers.BooleanField()
    status = serializers.CharField()
    description = serializers.CharField()
    tags = serializers.PrimaryKeyRelatedField(queryset=PostTag.objects.all(), many=True)
    # images = serializers.PrimaryKeyRelatedField(queryset=ImageFile.objects.all(), many=True)
    images = ImageFileSerializer(many=True)
    videos = VideoFileSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'author',
            'pub_date',
            'only_for_adult',
            'for_autenticated_users',
            'disable_comments',
            'status',
            'description',
            'tags',
            'images',
            'videos',
        )

    def update(self, instance: Post, validated_data):
        print(validated_data)
        if 'tags' not in validated_data:
            raise NotImplementedError("Update realization not supported for '{}'".format(validated_data))

        if self.partial:
            instance.tags.add( *validated_data['tags'] )
            instance.save()
        return instance
