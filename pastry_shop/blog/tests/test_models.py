import pytest

from faker import Faker

from pastry_shop.blog.models import Post, Comment

pytestmark = pytest.mark.django_db

fake = Faker()


class TestPostModel:
    def test_post_to_str(self, set_up):
        post = Post.objects.first()
        assert str(post) == post.title


class TestCommentModel:
    def test_comment_to_str(self, set_up):
        comment = Comment.objects.first()
        assert str(comment) == f"{comment.content[:20]} - {comment.author.username}"
