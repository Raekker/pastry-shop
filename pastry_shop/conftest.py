import pytest, random

from faker import Faker

from pastry_shop.shop.models import (
    Product,
    Category,
    Shop,
    Cart,
    ProductCart,
    Order,
    ProductOrder,
    Availability,
)
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
    cart = Cart.objects.create(client=author)
    for _ in range(3):
        post = Post.objects.create(
            title=fake.word(), content=fake.text(), author=author
        )
        Comment.objects.create(author=author, content=fake.text(), post=post)
        category = Category.objects.create(name=fake.word())
        product = Product.objects.create(
            name=fake.word(),
            description=fake.text(),
            price=random.random() * 10,
            amount=fake.pyint(min_value=1),
        )
        shop = Shop.objects.create(
            name=fake.word(), city=fake.city(), street=fake.address()
        )
        Availability.objects.create(
            shop=shop, product=product, amount=fake.pyint(min_value=1)
        )
        product.categories.add(category)
        ProductCart.objects.create(
            cart=cart, product=product, amount=fake.pyint(min_value=1)
        )
    order = Order.objects.create(client=author, status=1)
    for el in ProductCart.objects.filter(cart=cart):
        ProductOrder.objects.create(order=order, product=el.product, amount=el.amount)
