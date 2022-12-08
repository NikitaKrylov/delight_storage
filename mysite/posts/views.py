import json
from django.db.models import Q
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from .mixins import UpdateViewsMixin, PostQueryMixin, PostFilterFormMixin
from .models import Post, Comment
from .forms import PostTagsForm
from django.http import HttpResponse


def add_comment(request, *args, **kwargs):
    if request.method == "POST" and request.user.is_authenticated:
        post = Post.objects.get(pk=kwargs.get('pk'))
        comment = Comment(author=request.user, post=post,
                          text=request.POST['input-comments-form'])

        if "reply_comment_pk" in kwargs.values():
            comment.answered = Comment.objects.get(
                pk=kwargs['reply_comment_pk'])

        comment.save()
        return redirect(post)


class LikePostView(View):
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        ctx = {"liked": None}

        if request.user.is_authenticated:
            post = Post.objects.get(pk=kwargs['pk'])

            like, created = post.likes.get_or_create(user=request.user)
            if not created:  # already liked the content
                post.likes.remove(like)  # remove user from likes
                like.delete()
                ctx['liked'] = False
            else:
                post.likes.add(like)
                ctx['liked'] = True

        return HttpResponse(json.dumps(ctx), content_type='application/json')


class HomeView(TemplateView):
    template_name = 'posts/home.html'


class PostView(UpdateViewsMixin, PostFilterFormMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        context['videos'] = self.object.videos.all()
        context['tags'] = self.object.tags.all()
        context['comments'] = self.object.comments.all()
        context['title'] = "Пост {}".format(self.object.id)

        if self.request.user.is_authenticated and self.object.likes.filter(user=self.request.user).exists():
            context['like_active'] = '_active'
        else:
            context['like_active'] = ''

        return context


class PostList(PostQueryMixin, PostFilterFormMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/images.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = PostTagsForm(self.request.GET)
        context['title'] = "Посты"
        return context

    def get_queryset(self):
        response = super().get_queryset()
        form = PostTagsForm(self.request.GET)

        filter_query = Q()
        exclude_query = Q()

        for name, value in form.data.lists():
            if name == 'search':
                continue

            value = int(value[0])
            if value == 1:
                filter_query |= Q(tags__slug=name)
            elif value == -1:
                exclude_query |= Q(tags__slug=name)

        return response.exclude(exclude_query).filter(filter_query).distinct()


class LikedPostList(PostQueryMixin, PostFilterFormMixin, ListView):
    model = Post
    paginate_by = 20
    template_name = 'posts/images.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return super().get_queryset().filter(likes__user=self.request.user)
