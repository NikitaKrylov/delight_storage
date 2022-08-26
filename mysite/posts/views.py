from django.views.generic import DetailView, ListView, View

from .mixins import PostMixin, UpdateViewsMixin, PostListItemMixin
from .models import ImagePost, VideoPost, TextPost
from django.http import HttpResponse
from .services import update_post_views


class ImagePostView(UpdateViewsMixin, PostMixin, DetailView):
    model = ImagePost

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        post: ImagePost = self.get_object()
        return HttpResponse("<h1>{}</h1> <span>Pub date: {}</span> <h3>Author: {}</h3>".format(post, post.publication_date, post.post_author))


class VideoPostView(UpdateViewsMixin, PostMixin, DetailView):
    model = VideoPost


class TextPostView(UpdateViewsMixin, PostMixin, DetailView):
    model = TextPost


class ImagePostList(PostListItemMixin, ListView):
    model = ImagePost

    def get(self, request, *args, **kwargs):
        return HttpResponse(f"{[post.publication_date for post in self.get_queryset()]}")

