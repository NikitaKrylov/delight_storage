from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .serializers import PostTagSerializer, PostSerializer
from .models import PostTag, Post
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class PostTagList(generics.ListAPIView):
    serializer_class = PostTagSerializer

    def get_queryset(self):
        string = self.request.GET.get('operation', '').lower().split()
        if string:
            query = Q()
            for string in string:
                query |= Q(name__icontains=string)
            return PostTag.objects.filter(query)

        return PostTag.objects.all()


class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class UpdatePost(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]




