from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _

from pastry_shop.users.models import User


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=64)
    content = models.TextField(_("Content"))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(_("Content"))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.content[:20]} - {self.author.username}"
