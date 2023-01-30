import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Case, F, When, BooleanField, Exists, OuterRef, Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, DeleteView
from .forms import SearchForm
from .mixins import UpdateViewsMixin, PostQueryMixin, PostFilterFormMixin, AnnotateUserLikesAndViewsMixin
from .models import Post, Comment, PostTag, Like
from django.http import HttpResponse, Http404
from accounts.models import Subscription, User

from accounts.forms import ComplaintForm


class CreateComplaint(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        form = ComplaintForm(request.POST)

        if form.is_valid():
            post = Post.objects.get(pk=kwargs['pk'])

            complaint = form.save(commit=False)
            complaint.sender = request.user
            complaint.post = post
            complaint.save()

        return redirect(post)


def get_tags(request, *args, **kwargs):
    # needs split
    string = request.GET.get('operation').lower()
    ctx = {'tags':  list(PostTag.objects.filter(name__icontains=string).values("name", "slug").all())}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


class AddCommentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs.get('pk'))

        if post.disable_comments:
            raise ValueError("К этому посту нельзя оставлять комментарии")

        comment = Comment(author=request.user, post=post,
                          text=request.POST['input-comments-form'])

        comment.save()
        return redirect(comment.post)

    def get(self, request, *args, **kwargs):
        return redirect('post', pk=kwargs['pk'])


class AddReplyCommentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs.get('pk'))

        if post.disable_comments:
            raise ValueError("К этому посту нельзя оставлять комментарии")

        comment = Comment(author=request.user, post=post,
                          text=request.POST['reply-reply'])
        comment.answered = Comment.objects.get(
            pk=kwargs['reply_comment_pk'])

        comment.save()
        return redirect(comment.post)

    def get(self, request, *args, **kwargs):
        return redirect('post', pk=kwargs['pk'])


def delete_comment(request, *args, **kwargs):
    comment = Comment.objects.get(pk=kwargs['pk'])
    if request.user != comment.author:
        raise PermissionDenied()

    if request.user.is_authenticated and (request.user == comment.author or request.user.is_superuser):
        comment.delete()
    return redirect(comment.post)


@login_required()
def delete_post(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])

    if request.user != post.author:
        raise PermissionDenied()

    if request.user == post.author:
        post.delete()
    return redirect('post_list')


class LikePostView(View):
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        ctx = {"liked": None, "add_view": None}

        if request.user.is_authenticated:
            post = Post.objects.get(pk=kwargs['pk'])

            like, created = post.likes.get_or_create(user=request.user)
            if not created:  # already liked the content
                like.delete()
                ctx['liked'] = False
            else:
                post.likes.add(like)
                view, created = post.views.get_or_create(user=request.user)
                ctx['liked'] = True
                ctx['add_view'] = created

        return HttpResponse(json.dumps(ctx), content_type='application/json')


class HomeView(PostFilterFormMixin, TemplateView):
    template_name = 'posts/home.html'
    tags_batch_size = 20
    post_batch_size = 20
    author_batch_size = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_tags'] = PostTag.objects.best_by('likes')[
            :self.tags_batch_size]
        context['popular_posts'] = Post.objects.annotate(likes_count=Count(
            F('likes'))).order_by('-likes_count')[:self.post_batch_size]
        context['popular_authors'] = User.objects.annotate(subscribers_amount=Count(
            F('user_subscriptions'))).order_by('-subscribers_amount')[:self.author_batch_size]

        return context


class PostView(UpdateViewsMixin, PostFilterFormMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['complaint_form'] = ComplaintForm()
        context['images'] = self.object.images.all()
        context['videos'] = self.object.videos.all()
        context['tags'] = self.object.tags.all()
        context['comments'] = self.object.comments.all()
        context['title'] = "Пост {}".format(self.object.id)
        context['has_sub'] = False if not self.request.user.is_authenticated else Subscription.objects.filter(
            subscription_object=self.object.author, subscriber=self.request.user).exists()

        if self.request.user.is_authenticated and self.object.likes.filter(user=self.request.user).exists():
            context['like_active'] = '_active'
        else:
            context['like_active'] = ''

        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.is_authenticated:
            if self.object.author == request.user and self.object.status != Post.STATUS.PUBLISHED:
                return redirect('change_post', pk=self.object.pk)

            elif self.object.status != Post.STATUS.PUBLISHED:
                raise Http404

        return super().dispatch(request, *args, **kwargs)


class PostList(PostQueryMixin, AnnotateUserLikesAndViewsMixin, PostFilterFormMixin, ListView):
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


class SearchPostList(PostQueryMixin, AnnotateUserLikesAndViewsMixin, PostFilterFormMixin, ListView):
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

    def get_queryset(self):
        response = super().get_queryset().annotate(likes_amount=Count('likes', distinct=True), views_amount=Count('views', distinct=True))

        filter_query = Q()
        exclude_query = Q()

        for name, value in self.request.session['get_query'].items():

            if name == 'search':
                continue

            if name == 'sort_by':
                print(value)
            value = int(value)
            if value == 1:
                filter_query |= Q(tags__slug=name)
            elif value == -1:
                exclude_query |= Q(tags__slug=name)

        response = response.order_by('-likes_amount')
        # response = response.order_by('-views_amount')

        return response.exclude(exclude_query).filter(filter_query).distinct()


class PostCompilationList(PostQueryMixin, PostFilterFormMixin, ListView):
    model = Post
    paginate_by = 30
    template_name = 'posts/images.html'
    context_object_name = 'posts'

