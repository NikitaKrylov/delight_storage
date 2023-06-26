from rest_framework import serializers
from .models import User, Folder, FolderPost


class FolderPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = FolderPost
        fields = '__all__'


class FolderSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.username', required=False)
    posts = FolderPostSerializer(many=True, required=False)

    class Meta:
        model = Folder
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    folders = FolderSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'birth_date',
            'is_active',
            'is_superuser',
            'avatar',
            'folders',
        )




