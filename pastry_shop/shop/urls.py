from django.urls import path

from pastry_shop.shop.views import ProductListView, ProductDetailView

app_name = "shop"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]
