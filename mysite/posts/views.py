import json
from django.db.models import Q
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from .mixins import PostMixin, UpdateViewsMixin, PostListItemMixin
from .models import Post
from django.http import HttpResponse


class LikePostView(View):
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


class PostView(UpdateViewsMixin, PostMixin, DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        post: Post = self.get_object()
        return HttpResponse("<h1>{}</h1> <span>Pub date: {}</span> <h3>Author: {}</h3>".format(post, post.publication_date, post.author))


class PostList(PostListItemMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/images.html'
    context_object_name = 'posts'

    def get_queryset(self):
        search_terms: str = self.request.GET.get('search', '').split()
        response = super().get_queryset()

        if search_terms:
            query = Q()
            for item in search_terms:
                query |= Q(tags__name__startswith=item)
            response = response.filter(query).distinct()

        return response

