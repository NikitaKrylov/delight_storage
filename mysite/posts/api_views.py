from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PostTagSerializer, PostSerializer
from .models import PostTag, Post
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated


class PostTagViewSet(viewsets.ModelViewSet):
    serializer_class = PostTagSerializer
    queryset = PostTag.objects.all()

    @action(methods=['get'], detail=False)
    def filter(self, request, *args, **kwargs):
        string = self.request.GET.get('operation', '').lower().split()
        query = Q()
        for s in string:
            query |= Q(name__icontains=s)
        serializer = self.get_serializer(PostTag.objects.filter(query), many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

