from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from blog.models import Post

from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# @cache_page(300)
# @vary_on_cookie
def post_list(request):
    posts = Post.objects.filter(published_at__gt=datetime(2024,1,1)).select_related("author")
    logger.debug("%d posts available", len(posts))
    return render(request, "post_list.html", {"posts": posts})


def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, "post_detail.html", {"post": post})
