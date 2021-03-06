from django.urls import path

from pastry_shop.blog.views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostEditView,
    PostDeleteView,
    CommentEditView,
    CommentDeleteView,
)

app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/add/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/edit/", PostEditView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("comments/<int:pk>/edit/", CommentEditView.as_view(), name="comment-edit"),
    path(
        "comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
]
