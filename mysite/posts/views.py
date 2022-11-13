import json
from django.db.models import Q
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, FormView
from .mixins import UpdateViewsMixin, PostQueryMixin
from .models import Post
from .forms import PostTagsForm
from django.http import HttpResponse, HttpResponseRedirect


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


class PostView(UpdateViewsMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = list(self.object.images.all())
        context['tags'] = list(self.object.tags.all())
        context['comments'] = list(self.object.comments.all())

        return context


class PostList(PostQueryMixin, ListView):
    model = Post
    paginate_by = 5
    template_name = 'posts/images.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = PostTagsForm()
        return context

    def get_queryset(self):
        search_terms: str = self.request.GET.get('search', '').split()
        response = super().get_queryset()

        if search_terms:
            query = Q()
            for item in search_terms:
                query |= Q(tags__name__startswith=item)
            response = response.filter(query).distinct()

        return response
