from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]

