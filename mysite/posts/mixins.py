from django.db.models import Exists, OuterRef, Count, QuerySet

from accounts.models import ClientIP
from accounts.services.base import get_client_ip
from .forms import PostTagsForm, SearchForm
from .models import Post, Like, PostTag


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

        context['search_form'] = SearchForm(self.request.session.get('search_form', None))
        return context


class PostListMixin:
    annotate_views_and_likes = True
    check_availability = True
    mark_liked = True
    post_status: Post.STATUS = Post.STATUS.PUBLISHED

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            'likes',
            'views',
            'images',
            'videos',
        ).select_related('author')

        if self.annotate_views_and_likes:
            queryset = self._annotate_views_and_likes(queryset)

        if self.mark_liked:
            queryset = self._mark_liked(self.request,  queryset, self.request.user)

        if self.check_availability:
            queryset = self._check_availability(queryset, self.request.user)

        if self.post_status is not None:
            queryset = queryset.filter(status=self.post_status)

        return queryset

    @staticmethod
    def _annotate_views_and_likes(queryset: QuerySet[Post], order_by='-creation_date'):
        return queryset.annotate(
            views_amount=Count('views', distinct=True),
            likes_amount=Count('likes', distinct=True)
        ).order_by(order_by)

    @staticmethod
    def _mark_liked(request, queryset, user):
        if not user.is_authenticated:
            client_ip, created = ClientIP.objects.get_or_create(ip=get_client_ip(request))
            if created: return queryset
            filters = {'post': OuterRef('pk'), 'client_ip': client_ip}
        else:
            filters = {'post': OuterRef('pk'), 'user': user}

        return queryset.annotate(
            has_like=Exists(Like.objects.filter(**filters)),
        )

    @staticmethod
    def _check_availability(queryset, user):
        if user.is_authenticated:
            if not user.is_adult():
                queryset = queryset.exclude(only_for_adult=True)
        else:
            queryset = queryset.exclude(for_autenticated_users=True).exclude(only_for_adult=True)

        return queryset
