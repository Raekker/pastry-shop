from autoslug import AutoSlugField
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _

from pastry_shop.users.models import User


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Price"), max_digits=7, decimal_places=2)
    amount = models.IntegerField(_("Amount"))
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Cart(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="ProductCart")

    def get_total(self):
        total = 0
        for product in self.productcart_set.all():
            total += product.get_price()
        return total

    def __str__(self):
        return f"{self.client.username}'s cart({self.pk})"


class ProductCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def get_price(self):
        return self.amount * self.product.price


class Order(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, _("Pending")
        READY = 2, _("Ready for pickup")
        PAID = 3, _("Paid")
        DELIVERED = 4, _("Delivered")

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="ProductOrder")
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username}'s order({self.pk})"

    def get_total(self):
        total = 0
        for product in self.productorder_set.all():
            total += product.get_price()
        return total


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def get_price(self):
        return self.amount * self.product.price


class Shop(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    city = models.CharField(_("City"), max_length=100)
    street = models.CharField(_("Street"), max_length=100)
    products = models.ManyToManyField(Product, through="Availability")

    def __str__(self):
        return self.name


class Availability(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    amount = models.IntegerField()
