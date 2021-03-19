import pytest
from django.urls.base import reverse

from faker import Faker

from pastry_shop.shop.forms import ShopProductAddForm
from pastry_shop.shop.models import (
    Product,
    Category,
    Shop,
    Cart,
    Order,
    ProductCart,
    Availability,
)
from pastry_shop.users.models import User

pytestmark = pytest.mark.django_db

fake = Faker()


class TestProduct:
    def test_product_list(self, client, set_up):
        response = client.get(reverse("shop:product-list"))
        assert response.status_code == 200
        assert response.context["products"].count() == 3

    def test_product_detail(self, client, set_up):
        product = Product.objects.first()
        response = client.get(reverse("shop:product-detail", args=(product.pk,)))
        assert response.status_code == 200
        for attr in ("name", "description", "price", "amount"):
            assert hasattr(response.context["product"], attr)

    def test_cart_creation(self, client, set_up):
        new_client = User.objects.create_user(
            username="newTestClient", password="testpassword"
        )
        client.force_login(user=new_client)
        product = Product.objects.first()
        amount = 4
        response = client.post(
            reverse("shop:product-detail", args=(product.pk,)), {"amount": amount}
        )
        cart = Cart.objects.get(client=new_client)
        assert response.status_code == 302
        assert cart
        assert ProductCart.objects.filter(
            cart=cart, product=product, amount=amount
        ).exists()
        amount = ""
        response = client.post(
            reverse("shop:product-detail", args=(product.pk,)), {"amount": amount}
        )
        assert response.status_code == 200
        assert "form" in response.context

    def test_product_create(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        products_before = Product.objects.count()
        response = client.post(
            reverse("shop:product-create"),
            {
                "name": "testName",
                "description": "testDescription",
                "price": 4.53,
                "amount": 100,
                "categories": Category.objects.first().pk,
            },
        )
        assert response.status_code == 302
        assert products_before + 1 == Product.objects.count()

    def test_product_create_context_data(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        response = client.get(reverse("shop:product-create"))
        assert response.status_code == 200
        for key in ("action", "form"):
            assert key in response.context

    def test_product_edit(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        product = Product.objects.first()
        data = {
            "name": "newName",
            "description": product.description,
            "price": product.price,
            "amount": product.amount,
            "categories": Category.objects.first().pk,
        }
        response = client.post(reverse("shop:product-edit", args=(product.pk,)), data)
        product = Product.objects.get(pk=product.pk)
        assert response.status_code == 302
        assert product.name == "newName"

    def test_product_edit_context_data(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        product = Product.objects.first()
        response = client.get(reverse("shop:product-edit", args=(product.pk,)))
        assert response.status_code == 200
        for key in ("action", "form"):
            assert key in response.context

    def test_product_delete(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        product = Product.objects.first()
        products_before = Product.objects.count()
        response = client.delete(reverse("shop:product-delete", args=(product.pk,)))
        assert response.status_code == 302
        assert products_before - 1 == Product.objects.count()


class TestCategory:
    def test_category_list(self, client, set_up):
        response = client.get(reverse("shop:category-list"))
        assert response.status_code == 200
        assert response.context["categories"].count() == 3

    def test_category_detail(self, client, set_up):
        category = Category.objects.first()
        response = client.get(reverse("shop:category-detail", args=(category.slug,)))
        assert response.status_code == 200
        assert hasattr(response.context["category"], "product_set")

    def test_category_create(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        categories_before = Category.objects.count()
        response = client.post(reverse("shop:category-create"), {"name": fake.word()})
        assert response.status_code == 302
        assert categories_before + 1 == Category.objects.count()

    def test_category_create_context_data(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        response = client.get(reverse("shop:category-create"))
        assert response.status_code == 200
        for key in ("action", "form"):
            assert key in response.context

    def test_category_edit(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        category = Category.objects.first()
        response = client.post(
            reverse("shop:category-edit", args=(category.slug,)), {"name": "newName"}
        )
        category = Category.objects.get(pk=category.pk)
        assert response.status_code == 302
        assert category.name == "newName"

    def test_category_delete(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        category = Category.objects.first()
        categories_before = Category.objects.count()
        response = client.delete(reverse("shop:category-delete", args=(category.slug,)))
        assert response.status_code == 302
        assert categories_before - 1 == Category.objects.count()


class TestShop:
    def test_shop_list(self, client, set_up):
        response = client.get(reverse("shop:shop-list"))
        assert response.status_code == 200
        assert response.context["shops"].count() == 3

    def test_shop_detail(self, client, set_up):
        shop = Shop.objects.first()
        response = client.get(reverse("shop:shop-detail", args=(shop.pk,)))
        assert response.status_code == 200
        for attr in ("name", "city", "street"):
            assert hasattr(response.context["shop"], attr)

    def test_shop_create(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shops_before = Shop.objects.count()
        response = client.post(
            reverse("shop:shop-create"),
            {"name": "testName", "city": "testCity", "street": "testStreet"},
        )
        assert response.status_code == 302
        assert shops_before + 1 == Shop.objects.count()

    def test_shop_create_context_data(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        response = client.get(reverse("shop:shop-create"))
        assert response.status_code == 200
        for key in ("action", "form"):
            assert key in response.context

    def test_shop_edit(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shop = Shop.objects.first()
        response = client.post(
            reverse("shop:shop-edit", args=(shop.pk,)),
            {"name": "newName", "city": "newCity", "street": "newStreet"},
        )
        shop = Shop.objects.get(pk=shop.pk)
        assert response.status_code == 302
        assert shop.name == "newName"

    def test_shop_delete(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shop = Shop.objects.first()
        shops_before = Shop.objects.count()
        response = client.delete(reverse("shop:shop-delete", args=(shop.pk,)))
        assert response.status_code == 302
        assert shops_before - 1 == Shop.objects.count()

    def test_shop_product_add_same(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shop = Shop.objects.first()
        product = Product.objects.first()
        amount_before = shop.availability_set.get(product_id=product.pk).amount
        amount = 4
        response = client.post(
            reverse("shop:shop-product-add", args=(shop.pk,)),
            {"product": product.pk, "amount": amount},
        )
        assert response.status_code == 302
        assert (
            shop.availability_set.get(product_id=product.pk).amount
            == amount_before + amount
        )
        assert Availability.objects.filter(
            shop=shop, product=product, amount=amount_before + amount
        ).exists()

    def test_shop_product_add_different(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shop = Shop.objects.first()
        product = Product.objects.last()
        products_before = shop.products.count()
        amount = 4
        response = client.post(
            reverse("shop:shop-product-add", args=(shop.pk,)),
            {"product": product.pk, "amount": amount},
        )
        assert response.status_code == 302
        assert products_before + 1 == shop.products.count()
        assert Availability.objects.filter(
            shop=shop, product=product, amount=amount
        ).exists()

    def test_shop_product_add_wrong_data(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shop = Shop.objects.first()
        response = client.post(
            reverse("shop:shop-product-add", args=(shop.pk,)), {"amount": ""}
        )
        assert response.status_code == 200
        assert "form" in response.context

    def test_shop_product_add_get(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shop = Shop.objects.first()
        response = client.get(reverse("shop:shop-product-add", args=(shop.pk,)))
        assert response.status_code == 200
        assert "form" in response.context
        assert isinstance(response.context["form"], ShopProductAddForm)

    def test_shop_product_remove(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shop = Shop.objects.first()
        product = shop.products.first()
        products_before = shop.products.count()
        response = client.post(
            reverse("shop:shop-product-remove", args=(shop.pk, product.pk))
        )
        assert response.status_code == 302
        assert products_before - 1 == shop.products.count()

    def test_shop_product_remove_get(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        shop = Shop.objects.first()
        product = shop.products.first()
        response = client.get(
            reverse("shop:shop-product-remove", args=(shop.pk, product.pk))
        )
        assert response.status_code == 200
        assert "product" in response.context


class TestCart:
    def test_cart_detail(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        response = client.get(reverse("shop:cart-detail"))
        assert response.status_code == 200
        assert len(response.context["cart"].productcart_set.all()) == 3

    def test_cart_creation(self, client, set_up):
        new_client = User.objects.create_user(
            username="newTestClient", password="testpassword"
        )
        client.force_login(user=new_client)
        response = client.get(reverse("shop:cart-detail"))
        assert response.status_code == 200
        assert isinstance(response.context["cart"], Cart)

    def test_cart_add_product(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        product = Product.objects.last()
        cart = Cart.objects.get(client=User.objects.get(username="testUser"))
        products_before = cart.productcart_set.count()
        if cart.productcart_set.filter(product_id=product.pk).exists():
            amount_before = cart.productcart_set.get(product_id=product.pk).amount
        amount = 4
        response = client.post(
            reverse("shop:product-detail", args=(product.pk,)), {"amount": amount}
        )
        assert response.status_code == 302
        if cart.productcart_set.filter(product_id=product.pk).exists():
            assert (
                cart.productcart_set.get(product_id=product.pk).amount
                == amount_before + amount
            )
        else:
            assert products_before + 1 == cart.productcart_set.count()

    def test_cart_remove_product(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        product = Product.objects.first()
        cart = Cart.objects.get(client=User.objects.get(username="testUser"))
        products_before = cart.productcart_set.count()
        response = client.post(reverse("shop:cart-product-delete", args=(product.pk,)))
        assert response.status_code == 302
        assert products_before - 1 == cart.productcart_set.count()

    def test_cart_remove_get(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        product = Product.objects.first()
        cart = Cart.objects.get(client=User.objects.get(username="testUser"))
        response = client.get(reverse("shop:cart-product-delete", args=(product.pk,)))
        assert response.status_code == 200
        assert "product" in response.context
        assert cart


class TestOrder:
    def test_order_list(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        response = client.get(reverse("shop:order-list"))
        assert response.status_code == 200
        assert response.context["orders"].count() == 1

    def test_order_detail(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        order = Order.objects.filter(
            client=User.objects.get(username="testUser")
        ).first()
        response = client.get(reverse("shop:order-detail", args=(order.pk,)))
        assert response.status_code == 200
        assert hasattr(response.context["order"], "productorder_set")
        assert response.context["order"].productorder_set.count() == 3

    def test_order_create(self, client, set_up):
        client.force_login(user=User.objects.get(username="testUser"))
        response = client.post(reverse("shop:cart-detail"))
        cart = Cart.objects.get(client=User.objects.get(username="testUser"))
        assert response.status_code == 302
        assert cart.productcart_set.count() == 0
