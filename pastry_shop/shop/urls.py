from django.urls import path

from pastry_shop.shop.views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductEditView,
    ProductDeleteView,
    CategoryListView,
)

app_name = "shop"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/add/", ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/edit/", ProductEditView.as_view(), name="product-edit"),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
]
