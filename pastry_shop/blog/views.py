from django.db.models import QuerySet
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.views.generic.list import ListView

from pastry_shop.blog.models import Post


class MainPageView(View):
    def get(self, request):
        recent_posts = Post.objects.order_by("-created")
        return render(request, "pages/home.html", {"recent_posts": recent_posts})


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self) -> QuerySet:
        return Post.objects.order_by("-created")
