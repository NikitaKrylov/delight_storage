from .models import Post
from accounts.services import get_client_ip
from accounts.models import ClientIP


def update_post_views(request, post: Post):
    if post is None: return

    clien_ip, ip_created = ClientIP.objects.get_or_create(ip=get_client_ip(request))

    if ip_created and request.user.is_authenticated:
        """если ip до этого не был зарегестрирован и пользователь авторизован, 
        то просмотр мог быть создан только по пользователю"""
        user_view, created = post.views.get_or_create(user=request.user)
        user_view.client_ip = clien_ip
    else:
        """если ip уже был создан, 
        то по нему создавался просмотр;
        ищем просмотр и обновляем пользователя"""
        user_view, created = post.views.get_or_create(client_ip=clien_ip)
        user_view.user = request.user if request.user.is_authenticated else None

    """в любом случае обновляем пост так как поля могли быть обновлены"""
    user_view.save()

    if created: post.views.add(user_view)
