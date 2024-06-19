from rest_framework import generics

# from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.api.permissions import AuthorModifyOrReadOnly
from rest_framework.permissions import IsAdminUser

from blog.models import Post
from blango_auth.models import User
from blog.api.serializers import PostSerializer, UserSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer