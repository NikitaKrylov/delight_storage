from django.utils import timezone
from .celery import app
from posts.models import Post, PostDelay


@app.task
def publish_posts():
    posts = list(Post.objects.filter(status=1).filter(delay__time__lte=timezone.now()))

    for post in posts:
        post.status = 0
        post.pub_date = post.delay.time
        post.delay.delete()
        post.delay = None
        post.save(update_fields=['status', 'pub_date'])

    return f"\n--------------- Publish post, amount: {len(posts)} ---------------"

