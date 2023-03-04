from django.db.models import Exists, OuterRef, Count, F
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from .forms import PostTagsForm, SearchForm
from .models import Post, Like, PostTag
from .services.base import update_post_views


class PostFilterFormMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['session_tags'] = []

        if 'tags_query' in self.request.session:
            for key, value in self.request.session['tags_query'].items():
                context['session_tags'].append({
                    'name': PostTag.objects.get(slug=key).name,
                    'slug': key,
                    'value': value
                })
        # context['search_input'] = self.request.session.get('search_input', '')
        # context['sort_direction'] = self.request.session.get('sort_direction', '')
        # sort_type = self.request.session.get('sort_type', '')
        # context['sort_type'] = {'by-likes':'Лайкам', 'by-views': 'Просмотрам'}.get(sort_type, None) if sort_type else None
        context['search_form'] = SearchForm(self.request.session.get('search_form', None))
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


class AnnotateUserLikesAndViewsMixin(MultipleObjectMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                has_like=Exists(Like.objects.filter(post=OuterRef('pk'), user=self.request.user)),

            )
        return queryset.annotate(
            views_amount=Count('views', distinct=True),
            likes_amount=Count('likes', distinct=True)
        ).order_by('-creation_date')