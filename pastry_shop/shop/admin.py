from django.contrib import admin
from .models import Product, Category, Shop, Order, Cart, ProductCart, ProductOrder


# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


class ProductCartInline(admin.TabularInline):
    model = ProductCart


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("pk", "client")
    inlines = [
        ProductCartInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "street")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "client", "created")
    inlines = [
        ProductOrderInline,
    ]
