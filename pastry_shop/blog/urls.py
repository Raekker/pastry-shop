from django.urls import path

from pastry_shop.blog.views import PostListView

app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
]
