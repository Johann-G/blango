from django.contrib import admin
from blog.models import Tag, Post, Comment, AuthorProfile


class TagAdmin(admin.ModelAdmin):
    list_display = ["value"]


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["slug", "published_at"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["content"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AuthorProfile)