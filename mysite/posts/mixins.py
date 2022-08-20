from django.views.generic.detail import SingleObjectMixin
from .models import ImagePost, VideoPost, TextPost, AbstractBasePost


class PostMixin(SingleObjectMixin):
    model = AbstractBasePost
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context['pub_date'] = post.publication_date
        context['post_author'] = post.post_author
        context['tags'] = list(post.tags.all())
        context['comments'] = list(post.comments.all())
        context['average_mark'] = post.average_mark()

        return context


class CheckPermissionsMixin:
    pass