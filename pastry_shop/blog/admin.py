from django.contrib import admin
from .models import Post, Comment

# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_filter = ("created", "modified")
    inlines = [
        CommentInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author")
    list_filter = ("created", "modified")
