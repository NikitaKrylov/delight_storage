import sys

from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from sklearn.metrics import jaccard_score

from accounts.services.base import get_client_ip
from mysite.services import ajax_require
from .forms import SearchForm, CreatePostTagForm
from .services.base import update_post_views, update_post_like
from .services.clustering import TagsVectorizer, PostClustering

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q, F, Count
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView, DeleteView

from .mixins import PostFilterFormMixin, PostListMixin
from .models import Post, Comment, PostTag
from django.http import Http404, JsonResponse
from accounts.models import Subscription, User, ClientIP

from accounts.forms import ComplaintForm, UserFolderForm


@login_required
@require_http_methods(['POST'])
def create_post_complain(request, *args, **kwargs):
    form = ComplaintForm(request.POST)

    if form.is_valid():
        post = Post.objects.get(pk=kwargs['pk'])
        complaint = form.save(commit=False)
        complaint.sender = request.user
        complaint.post = post
        complaint.save()
        return redirect(post)

    raise ValidationError()


@ajax_require
@require_http_methods(['GET'])
def get_tags(request, *args, **kwargs):
    """Returns Json object with list of dicts contains the name and slug of the tags
     by the requested names"""

    strings: str = request.GET.get('operation').lower().split()

    if strings:
        query = Q()
        for string in strings:
            query |= Q(name__icontains=string)

        ctx = {'tags': list(PostTag.objects.filter(
            query).values("name", "slug"))}
    else:
        ctx = {'tags': list()}

    return JsonResponse(ctx)


@ajax_require
@require_http_methods(['POST'])
def create_post_tag(request, *args, **kwargs):
    """Ajax's method which creates tag by the CreatePostTagForm"""
    form = CreatePostTagForm(request.POST)

    if form.is_valid():
        tag: PostTag = form.save()
        tag.save()
        return JsonResponse({'id': tag.id, 'name': tag.name, 'slug': tag.slug})

    response = JsonResponse({"errors": list(form.errors.values())})
    response.status_code = 403
    return response


@login_required
@require_http_methods(['POST'])
def create_post_comment(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs.get('pk'))

    if post.disable_comments:
        raise ValueError(
            "К этому посту нельзя оставлять комментарии")

    comment = Comment(author=request.user, post=post,
                      text=request.POST['input-comments-form'])
    comment.save()
    return redirect(comment.post)


def create_reply_post_comment(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs.get('pk'))

    if post.disable_comments:
        raise ValueError(
            "К этому посту нельзя оставлять комментарии")

    comment = Comment(author=request.user, post=post,
                      text=request.POST['reply-reply'])
    comment.answered = Comment.objects.get(
        pk=kwargs['reply_comment_pk'])

    comment.save()
    return redirect(comment.post)


def delete_comment(request, *args, **kwargs):
    comment = get_object_or_404(Comment, pk=kwargs['pk'])

    if request.user.is_authenticated and (request.user == comment.author or request.user.is_superuser):
        comment.delete()
        messages.success(request, 'Комментарий удален')
    else:
        raise PermissionDenied("Вы не являетесь автором комментария")

    return redirect(comment.post)


@login_required
def delete_post(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])

    if request.user != post.author:
        raise PermissionDenied()

    if request.user == post.author:
        post.delete()

    return redirect('self_user_posts')


@ajax_require
@require_http_methods(['POST', 'GET'])
def like_post(request, *args, **kwargs):
    post = get_object_or_404(Post, pk=kwargs['pk'])
    ctx = update_post_like(request, post)
    return JsonResponse(ctx)


class HomeView(PostFilterFormMixin, TemplateView):
    template_name = 'posts/home.html'
    tags_batch_size = 20
    post_batch_size = 20
    author_batch_size = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная"
        context['popular_tags'] = PostTag.objects.best_by('likes')[
            :self.tags_batch_size]
        context['popular_posts'] = Post.objects.annotate(likes_count=Count(
            F('likes'))).order_by('-likes_count')[:self.post_batch_size]
        context['popular_authors'] = User.objects.annotate(subscribers_amount=Count(
            F('user_subscriptions'))).order_by('-subscribers_amount')[:self.author_batch_size]

        return context


class PostDetailView(PostFilterFormMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['complaint_form'] = ComplaintForm()
        context['folder_form'] = UserFolderForm()
        context['title'] = "Пост {}".format(self.object.id)
        context['has_sub'] = False if not self.request.user.is_authenticated else Subscription.objects.filter(
            subscription_object=self.object.author, subscriber=self.request.user).exists()

        client_ip = ClientIP.objects.filter(ip=get_client_ip(self.request))
        if (self.request.user.is_authenticated and self.object.likes.filter(user=self.request.user).exists()) or (client_ip.exists() and self.object.likes.filter(client_ip=client_ip.first()).exists()):
            context['like_active'] = '_active'
        else:
            context['like_active'] = ''

        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            if self.object.author == request.user and self.object.status != Post.STATUS.PUBLISHED:
                return redirect('change_post', pk=self.object.pk)

            elif self.object.status != Post.STATUS.PUBLISHED:
                raise Http404()

        update_post_views(request, self.object)
        return response


class PostList(PostListMixin, PostFilterFormMixin, ListView):
    model = Post
    paginate_by = 30
    template_name = 'posts/images.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        if request.GET:
            request.session['get_query'] = request.GET
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = "Посты"
        return context


class SearchPostList(PostListMixin, PostFilterFormMixin, ListView):
    model = Post
    paginate_by = 30
    template_name = 'posts/images.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        responce: dict = request.GET.dict()
        form = SearchForm(request.GET)
        [responce.pop(i) for i in form.fields.keys() if i in responce]

        request.session['tags_query'] = dict(filter(lambda pair: pair[1] != '0', responce.items()))
        request.session['search_form'] = form.data.dict()

        if not request.session['tags_query']:
            return redirect('post_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = "Посты"
        return context

    def get_queryset(self):
        response = super().get_queryset()

        filter_query = Q()
        exclude_query = Q()

        for name, value in self.request.session['tags_query'].items():

            if name == 'search':
                continue

            if name == 'sort_by':
                continue

            value = int(value)
            if value == 1:
                filter_query |= Q(tags__slug=name)
            elif value == -1:
                exclude_query |= Q(tags__slug=name)

        search_form = SearchForm(self.request.session.get('search_form', None))
        order = search_form.data.get('type', 'pub_date')
        direction = search_form.data.get('is_desc', '')
        response = response.order_by(direction + order)
        # if sort_type == 'by-likes':
        #     response = response.order_by('{}likes_amount'.format(sort_direction))
        # elif sort_type == 'by-views':
        #     response = response.order_by('{}views_amount'.format(sort_direction))

        return response.exclude(exclude_query).filter(filter_query).distinct()


class SearchPostTagListView(PostListMixin, PostFilterFormMixin, ListView):
    model = Post
    paginate_by = 30
    template_name = 'posts/images.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs['slug'])


class PostCompilationsList(PostFilterFormMixin, TemplateView):
    template_name = 'posts/compilations.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostCompilationsList,
                        self).get_context_data(*args, **kwargs)
        context['title'] = "Подборки"
        context['clusters'] = PostClustering().fit(Post.objects.all())
        return context

