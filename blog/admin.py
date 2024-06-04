from django.contrib import admin
from blog.models import Tag, Post


class TagAdmin(admin.ModelAdmin):
    list_display = ["value"]


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["slug", "published_at"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)