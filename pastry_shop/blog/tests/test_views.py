import pytest

from faker import Faker

from pastry_shop.blog.models import Post
from pastry_shop.users.models import User

pytestmark = pytest.mark.django_db

fake = Faker()


class TestMainPage:
    def test_main_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "recent_posts" in response.context
        assert len(response.context["recent_posts"]) <= 3


class TestPost:
    def test_post_list(self, client, set_up):
        response = client.get("/blog/posts/")
        assert response.status_code == 200
        assert "posts" in response.context
        assert len(response.context["posts"]) == 3

    def test_post_detail(self, client, set_up):
        post = Post.objects.first()
        response = client.get(f"/blog/posts/{post.pk}/")
        assert response.status_code == 200
        assert len(response.context["post"].comments.all()) == 1
        for key in ("title", "content", "author", "created"):
            assert hasattr(response.context["post"], key)

    def test_post_create(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        response = client.post(
            "/blog/posts/add/", {"title": fake.word(), "content": fake.text()}
        )
        assert response.status_code == 302

    def test_post_delete(self, client, set_up):
        posts_before = len(Post.objects.all())
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        response = client.delete(f"/blog/posts/{post.pk}/delete/")
        assert response.status_code == 302
        assert posts_before - 1 == len(Post.objects.all())

    def test_post_update(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        new_title = "testTitle"
        new_content = "testContent"
        response = client.post(
            f"/blog/posts/{post.pk}/edit/", {"title": new_title, "content": new_content}
        )
        assert response.status_code == 302


class TestComment:
    def test_comment_list(self, client, set_up):
        post = Post.objects.first()
        response = client.get(f"/blog/posts/{post.pk}/")
        assert response.status_code == 200
        assert len(response.context["post"].comments.all()) == 1

    def test_comment_create(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        comment_content = "testContent"
        response = client.post(f"/blog/posts/{post.pk}/", {"content": comment_content})
        assert response.status_code == 302

    def test_comment_edit(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        comment_content = "testContent"
        comment = post.comments.first()
        response = client.post(
            f"/blog/comments/{comment.pk}/edit/", {"content": comment_content}
        )
        assert response.status_code == 302

    def test_comment_delete(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        post = Post.objects.first()
        comment = post.comments.first()
        response = client.delete(f"/blog/comments/{comment.pk}/delete/")
        assert response.status_code == 302
