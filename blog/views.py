from django.shortcuts import render
from blog.models import Post

import logging

logger = logging.getLogger(__name__)


def post_list(request):
    posts = Post.objects.all()
    logger.debug("%d posts available", len(posts))
    return render(request, "post_list.html", {"posts": posts})


def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, "post_detail.html", {"post": post})
