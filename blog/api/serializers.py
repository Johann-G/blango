from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
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