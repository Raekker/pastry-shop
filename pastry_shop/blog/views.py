from typing import Any, Dict

from django.db.models import QuerySet
from django.forms.models import BaseModelForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from pastry_shop.blog.forms import PostForm
from pastry_shop.blog.models import Post
from pastry_shop.users.models import User


class MainPageView(View):
    def get(self, request):
        recent_posts = Post.objects.order_by("-created")[:3]
        return render(request, "pages/home.html", {"recent_posts": recent_posts})


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self) -> QuerySet:
        return Post.objects.order_by("-created")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_form.html"
    form_class = PostForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse("blog:post-list")


class PostEditView(UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    form_class = PostForm

    def get_success_url(self) -> str:
        return reverse("blog:post-detail", kwargs={"pk": self.kwargs.get("pk")})


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"

    def get_success_url(self) -> str:
        return reverse("blog:post-list")
