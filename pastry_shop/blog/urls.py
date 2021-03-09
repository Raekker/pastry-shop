from django.urls import path

from pastry_shop.blog.views import PostListView, PostDetailView

app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
]
