from autoslug import AutoSlugField
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _

from pastry_shop.users.models import User


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = AutoSlugField(populate_from="name")


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Price"), max_digits=7, decimal_places=2)
    amount = models.IntegerField(_("Amount"))
    categories = models.ManyToManyField(Category)


class Cart(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="ProductCart")


class ProductCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Order(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, _("Pending")
        READY = 2, _("Ready for pickup")
        PAID = 3, _("Paid")
        DELIVERED = 4, _("Delivered")

    client = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="ProductOrder")
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Shop(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    city = models.CharField(_("City"), max_length=100)
    street = models.CharField(_("Street"), max_length=100)
    products = models.ManyToManyField(Product, through="Availability")


class Availability(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    amount = models.IntegerField()
