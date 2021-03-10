from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView

from pastry_shop.shop.models import Product


class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 5
