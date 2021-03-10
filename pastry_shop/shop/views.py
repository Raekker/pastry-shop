from typing import Any, Dict

from django.shortcuts import render

# Create your views here.
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from pastry_shop.shop.forms import ProductForm
from pastry_shop.shop.models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 5


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    template_name = "shop/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("shop:product-list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context["action"] = "create"
        return context


class ProductEditView(UpdateView):
    model = Product
    template_name = "shop/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("shop:product-list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductEditView, self).get_context_data(**kwargs)
        context["action"] = "edit"
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "shop/product_confirm_delete.html"
    success_url = reverse_lazy("shop:product-list")


class CategoryListView(ListView):
    model = Category
    template_name = "shop/category_list.html"
    context_object_name = "categories"
