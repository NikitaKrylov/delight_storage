from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from .models import Post
from .services import update_post_views


class PostQueryMixin(MultipleObjectMixin):
    model = Post

    def get_queryset(self):
        queryset = self.model.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(for_autenticated_users=False)
            queryset = queryset.filter(only_for_adult=False)

        elif not self.request.user.is_adult():
            queryset = queryset.filter(only_for_adult=False)

        return queryset


class UpdateViewsMixin(SingleObjectMixin):
    """Inherited before PostMixin"""
    def get(self, request, *args, **kwargs):
        update_post_views(request, self.get_object())
        return super().get(request, *args, **kwargs)