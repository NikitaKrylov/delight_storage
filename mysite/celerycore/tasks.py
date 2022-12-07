from .celery import app
from posts.models import Post, PostDelay
from datetime import datetime


@app.task
def publish_posts():
    posts = list(Post.objects.filter(status=1).filter(delay__time__lte=datetime.now()))

    for post in posts:
        post.status = 0
        post.pub_date = post.delay.time
        post.delay.delete()
        post.delay = None
        post.save(update_fields=['status', 'pub_date'])

    return f"\n--------------- Publish post, amount: {len(posts)} ---------------"

