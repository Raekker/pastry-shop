from django.urls import path

from pastry_shop.shop.views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductEditView,
    ProductDeleteView,
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryEditView,
    CategoryDeleteView,
    ShopListView,
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
    path(
        "category/<slug:slug>/products",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path("category/add", CategoryCreateView.as_view(), name="category-create"),
    path("category/<slug:slug>/edit", CategoryEditView.as_view(), name="category-edit"),
    path(
        "category/<slug:slug>/delete",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path("shops/", ShopListView.as_view(), name="shop-list"),
]
