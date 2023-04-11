from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PostTagSerializer, PostSerializer
from .models import PostTag, Post
from rest_framework import generics, viewsets


class PostTagViewSet(viewsets.ModelViewSet):
    serializer_class = PostTagSerializer
    queryset = PostTag.objects.all()
    lookup_field = 'slug'

    @action(methods=['get'], detail=False)
    def filter(self, request, *args, **kwargs):
        query = Q()
        st = self.request.GET.get('operation', '').lower().split()

        if not st:
            return Response([])

        for s in st:
            query |= Q(name__icontains=s)

        serializer = self.get_serializer(PostTag.objects.filter(query), many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

