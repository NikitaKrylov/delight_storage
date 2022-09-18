import json

from django.views import View
from django.views.generic import DetailView, ListView
from .mixins import PostMixin, UpdateViewsMixin, PostListItemMixin
from .models import ImagePost, VideoPost, TextPost, Like
from django.http import HttpResponse


class LikePostView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            post = ImagePost.objects.get(pk=kwargs['pk'])

            like, created = post.likes.get_or_create(user=request.user)
            if not created:  # already liked the content
                post.likes.remove(like)  # remove user from likes
                like.delete()
                liked = False
            else:
                post.likes.add(like)
                liked = True

            ctx = {"liked": liked}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        return super().get(request, *args, **kwargs)


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
    paginate_by = 10
    template_name = 'posts/images.html'
    context_object_name = 'posts'

