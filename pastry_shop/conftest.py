import pytest

from faker import Faker

from pastry_shop.shop.models import Product
from pastry_shop.users.models import User
from pastry_shop.users.tests.factories import UserFactory
from pastry_shop.blog.models import Post, Comment


fake = Faker()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def set_up():
    author = User.objects.create_user(
        username="testUser",
        password="testpassword",
        email="test@gmail.com",
        is_superuser=True,
    )
    for _ in range(3):
        post = Post.objects.create(
            title=fake.word(), content=fake.text(), author=author
        )
        Comment.objects.create(author=author, content=fake.text(), post=post)
