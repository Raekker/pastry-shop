import pytest
from django.urls.base import reverse, resolve

from faker import Faker

from pastry_shop.blog.models import Post, Comment
from pastry_shop.users.models import User

pytestmark = pytest.mark.django_db

fake = Faker()


class TestMainPage:
    def test_main_page(self, client):
        response = client.get(reverse("home"))
        assert response.status_code == 200
        assert "recent_posts" in response.context
        assert 0 <= len(response.context["recent_posts"]) <= 3


class TestPost:
    def test_post_list(self, client, set_up):
        response = client.get(reverse("blog:post-list"))
        assert response.status_code == 200
        assert "posts" in response.context
        assert len(response.context["posts"]) == 3

    def test_post_detail(self, client, set_up):
        post = Post.objects.first()
        response = client.get(reverse("blog:post-detail", args=(post.pk,)))
        assert response.status_code == 200
        assert len(response.context["post"].comments.all()) == 1
        for attr in ("title", "content", "author", "created"):
            assert hasattr(response.context["post"], attr)

    def test_post_create(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        posts_before = Post.objects.count()
        response = client.post(
            reverse("blog:post-create"), {"title": fake.word(), "content": fake.text()}
        )
        assert response.status_code == 302
        assert posts_before + 1 == Post.objects.count()

    def test_post_delete(self, client, set_up):
        posts_before = Post.objects.count()
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        response = client.delete(reverse("blog:post-delete", args=(post.pk,)))
        assert response.status_code == 302
        assert posts_before - 1 == Post.objects.count()

    def test_post_update(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        new_title = fake.word()
        new_content = fake.text()
        response = client.post(
            reverse("blog:post-edit", args=(post.pk,)),
            {"title": new_title, "content": new_content},
        )
        post = Post.objects.get(pk=post.pk)
        assert response.status_code == 302
        assert post.title == new_title
        assert post.content == new_content


class TestComment:
    def test_comment_list(self, client, set_up):
        post = Post.objects.first()
        response = client.get(reverse("blog:post-detail", args=(post.pk,)))
        assert response.status_code == 200
        assert response.context["post"].comments.count() == 1

    def test_comment_create(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        comments_before = post.comments.count()
        comment_content = fake.word()
        response = client.post(
            reverse("blog:post-detail", args=(post.pk,)), {"content": comment_content}
        )
        assert response.status_code == 302
        assert comments_before + 1 == post.comments.count()

    def test_comment_post_wrong_data(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        response = client.post(
            reverse("blog:post-detail", args=(post.pk,)), {"content": ""}
        )
        assert response.status_code == 200
        assert "form" in response.context

    def test_comment_edit(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        comment_content = fake.word()
        comment = post.comments.first()
        response = client.post(
            reverse("blog:comment-edit", args=(comment.pk,)),
            {"content": comment_content},
        )
        comment = Comment.objects.get(pk=comment.pk)
        assert response.status_code == 302
        assert comment.content == comment_content

    def test_comment_delete(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        comments_before = post.comments.count()
        comment = post.comments.first()
        response = client.delete(reverse("blog:comment-delete", args=(comment.pk,)))
        assert response.status_code == 302
        assert comments_before - 1 == post.comments.count()
