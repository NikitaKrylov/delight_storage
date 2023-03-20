from django.db.models import Q
from .serializers import PostTagSerializer
from .models import PostTag
from rest_framework import generics


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
