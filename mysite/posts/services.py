from .models import Post
from accounts.services import get_client_ip
from accounts.models import ClientIP

from accounts.models import User


def update_post_views(request, post: Post):
    if post is None: return
    user = request.user

    if user.is_authenticated:
        user_view, created = post.views.get_or_create(user=user)
    else:
        clien_ip, ip_created = ClientIP.objects.get_or_create(ip=get_client_ip(request))
        user_view, created = post.views.get_or_create(client_ip=clien_ip)

