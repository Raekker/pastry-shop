from typing import Any, Dict, Type, Optional

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.list import ListView

from pastry_shop.blog.forms import PostForm, CommentForm
from pastry_shop.blog.models import Post, Comment
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


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    form_class = CommentForm

    def get_success_url(self) -> str:
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: BaseForm) -> HttpResponse:
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.object
        comment.save()
        return redirect(self.get_success_url())


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "blog.add_post"
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


class PostEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "blog.change_post"
    model = Post
    template_name = "blog/post_form.html"
    form_class = PostForm

    def get_success_url(self) -> str:
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "blog.delete_post"
    model = Post
    template_name = "blog/post_confirm_delete.html"

    def get_success_url(self) -> str:
        return reverse("blog:post-list")


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = "blog/comment_form.html"
    form_class = CommentForm

    def get_success_url(self) -> str:
        return reverse("blog:post-detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self) -> str:
        return reverse("blog:post-detail", kwargs={"pk": self.object.post.pk})
