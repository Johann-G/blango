from rest_framework import generics, viewsets
# from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.api.permissions import AuthorModifyOrReadOnly
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.http import Http404
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from blog.models import Post, Tag
from blango_auth.models import User
from blog.api.serializers import PostSerializer, PostDetailSerializer, UserSerializer, TagSerializer


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUser]
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = self.queryset.filter(published_at__lte=timezone.now())
        
        if self.request.user.is_staff:
            queryset = self.queryset
        
        queryset = self.queryset.filter(
            Q(published_at__lte=timezone.now()) | Q(author=self.request.user)
        )

        period_name = self.kwargs.get("period_name")

        if not period_name:
            return queryset
    
        if period_name == "new":
            return queryset.filter(published_at__gte=timezone.now() - timedelta(hours=1))
        elif period_name == "today":
            return queryset.filter(published_at__gte=timezone.now() - timedelta(days=1))
        elif period_name == "week":
            return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
        else:
            raise Http404(
                f"Time period {period_name} should be 'new', 'today', 'week'"
            )
    
    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Authorization", "Cookie"))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
    
    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    @method_decorator(vary_on_headers("Authorization"))
    @action(methods=["get"], detail=False, name="Posts by the logged in user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Posts are yours")
        posts = self.get_queryset().filter(author=request.user)
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @method_decorator(cache_page(60))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @method_decorator(cache_page(60))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @method_decorator(cache_page(60))
    @action(methods=["get"], detail=True, name="Posts with the tag")
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(tag.posts, many=True, context={"request": request})
        return Response(post_serializer.data)