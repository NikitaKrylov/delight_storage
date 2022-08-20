from django.views.generic import DetailView, ListView, View

from .mixins import PostMixin
from .models import ImagePost, VideoPost, TextPost
from django.http import HttpResponse


class ImagePostView(PostMixin, DetailView):
    model = ImagePost

    def get(self, request, *args, **kwargs):
        object: ImagePost = self.get_object()
        return HttpResponse("<h1>{}</h1> <span>Pub date: {}</span> <h3>Author: {}</h3>".format(object, object.publication_date, object.post_author))


class VideoPostView(DetailView):
    model = VideoPost


class TextPostView(DetailView):
    model = TextPost


class ImagePostList(ListView):
    model = ImagePost

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(for_autenticated_users=False)
        return queryset

    def get(self, request, *args, **kwargs):
        return HttpResponse(f"{[post.publication_date for post in self.get_queryset()]}")

