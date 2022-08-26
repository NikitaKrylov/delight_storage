from .models import AbstractBasePost
from accounts.services import get_client_ip
from accounts.models import ClientIP


def update_post_views(request, post: AbstractBasePost):
    if post is None: return

    string_ip = get_client_ip(request)
    clien_ip, created = ClientIP.objects.get_or_create(ip=string_ip)

    if created or not post.views.filter(ip=string_ip).exists():
        post.views.add(clien_ip)
