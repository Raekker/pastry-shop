import pytest

from pastry_shop.shop.models import Product, Category, Shop, Cart, Order

pytestmark = pytest.mark.django_db


def test_category_to_str(set_up):
    category = Category.objects.first()
    assert str(category) == category.name


def test_product_to_str(set_up):
    product = Product.objects.first()
    assert str(product) == product.name


def test_cart_to_str(set_up):
    cart = Cart.objects.first()
    assert str(cart) == f"{cart.client.username}'s cart({cart.pk})"


def test_order_to_str(set_up):
    order = Order.objects.first()
    assert str(order) == f"{order.client.username}'s order({order.pk})"


def test_shop_to_str(set_up):
    shop = Shop.objects.first()
    assert str(shop) == shop.name
