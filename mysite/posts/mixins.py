from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from .forms import PostTagsForm
from .models import Post
from .services import update_post_views


class PostFilterFormMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = PostTagsForm(self.request.session.get('get_query', None))
        return context


class PostQueryMixin(MultipleObjectMixin):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            if not user.is_adult():
                queryset = queryset.filter(only_for_adult=False)
            queryset = queryset.exclude(tags__in=user.ignored_tags.all())
        else:
            queryset = queryset.filter(for_autenticated_users=False).filter(only_for_adult=False)

        return queryset.filter(status=Post.STATUS.PUBLISHED)


class UpdateViewsMixin(SingleObjectMixin):
    """Inherited before PostMixin"""
    def get(self, request, *args, **kwargs):
        update_post_views(request, self.get_object())
        return super().get(request, *args, **kwargs)