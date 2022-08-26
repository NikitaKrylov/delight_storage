from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .models import AbstractBasePost
from .services import update_post_views


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
        context['views_amount'] = post.count_views()
        context['likes_amount'] = post.count_likes()

        return context


class PostListItemMixin(MultipleObjectMixin):
    model = AbstractBasePost

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(for_autenticated_users=False)

        if not self.request.user.is_adult():
            queryset = queryset.filter(only_for_adult=False)

        return queryset


class UpdateViewsMixin(SingleObjectMixin):
    """Inherited before PostMixin"""
    def get(self, request, *args, **kwargs):
        update_post_views(request, self.get_object())
        return super().get(request, *args, **kwargs)