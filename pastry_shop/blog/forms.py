from django import forms

from pastry_shop.blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
