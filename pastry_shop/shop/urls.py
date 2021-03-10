from django.urls import path

from pastry_shop.shop.views import ProductListView

app_name = "shop"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
]
