from rest_framework import serializers
from blog.models import Post, Tag
from blango_auth.models import User


class PostSerializer(serializers.ModelSerializer):

    tags = serializers.SlugRelatedField(slug_field="value", many=True, queryset=Tag.objects.all())
    author = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name="api_user_detail", lookup_field="email")

    class Meta:
        model = Post
        fields = "__all__"
        readonly = ["modified_at", "created_at"]

    def validate_title(self, value):
        if value[0] == value[0].lower():
            raise serializers.ValidationError("Title first letter must be capitalized")
        return value

    def validate(self, data):
        if data["title"] not in data["summary"]:
            raise serializers.ValidationError("Title must be in the summary")
        return data
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email"]