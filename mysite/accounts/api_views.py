from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, Folder
from .serializers import UserSerializer, FolderSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]


class UserFolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.folders.filter(name=request.data['name']).exists():
            raise ValidationError("Папка с таким названием уже существует")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





