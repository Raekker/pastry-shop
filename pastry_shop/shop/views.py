from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render, redirect

# Create your views here.
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from pastry_shop.shop.forms import ProductForm, CartProductAddForm, ShopProductAddForm
from pastry_shop.shop.models import (
    Product,
    Category,
    Shop,
    Cart,
    ProductCart,
    Order,
    ProductOrder,
    Availability,
)


class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 5


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["form"] = CartProductAddForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CartProductAddForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.filter(client=self.request.user)
            if not cart:
                Cart.objects.create(client=self.request.user)
            cart = Cart.objects.get(client=self.request.user)
            product = Product.objects.get(pk=kwargs.get("pk"))
            if cart.productcart_set.filter(product_id=product.pk).exists():
                product_cart = cart.productcart_set.get(product_id=product.pk)
                product_cart.amount += form.cleaned_data["amount"]
                product_cart.save()
            else:
                product_cart = ProductCart()
                product_cart.cart = cart
                product_cart.product = product
                product_cart.amount = form.cleaned_data["amount"]
                product_cart.save()
            return redirect("shop:cart-detail")
        return render(request, "shop/product_detail.html", {"form": form})


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "shop.add_product"
    model = Product
    template_name = "shop/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("shop:product-list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context["action"] = "create"
        return context


class ProductEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "shop.change_product"
    model = Product
    template_name = "shop/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("shop:product-list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductEditView, self).get_context_data(**kwargs)
        context["action"] = "edit"
        return context


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "shop.delete_product"
    model = Product
    template_name = "shop/product_confirm_delete.html"
    success_url = reverse_lazy("shop:product-list")


class CategoryListView(ListView):
    model = Category
    template_name = "shop/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "shop/category_detail.html"


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "shop.add_category"
    model = Category
    fields = ("name",)
    template_name = "shop/category_form.html"
    success_url = reverse_lazy("shop:category-list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context["action"] = "create"
        return context


class CategoryEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "shop.change_category"
    model = Category
    fields = ("name",)
    template_name = "shop/category_form.html"
    success_url = reverse_lazy("shop:category-list")


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "shop.delete_category"
    model = Category
    template_name = "shop/category_confirm_delete.html"
    success_url = reverse_lazy("shop:category-list")


class ShopListView(ListView):
    model = Shop
    template_name = "shop/shop_list.html"
    context_object_name = "shops"


class ShopDetailView(DetailView):
    model = Shop
    template_name = "shop/shop_detail.html"


class ShopCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "shop.add_shop"
    model = Shop
    fields = ("name", "city", "street")
    template_name = "shop/shop_form.html"
    success_url = reverse_lazy("shop:shop-list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ShopCreateView, self).get_context_data(**kwargs)
        context["action"] = "create"
        return context


class ShopEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "shop.change_shop"
    model = Shop
    fields = ("name", "city", "street")
    template_name = "shop/shop_form.html"
    success_url = reverse_lazy("shop:shop-list")


class ShopDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "shop.delete_shop"
    model = Shop
    template_name = "shop/shop_confirm_delete.html"
    success_url = reverse_lazy("shop:shop-list")


class CartDetailView(View):
    def get(self, request, *args, **kwargs):

        cart = Cart.objects.filter(client=self.request.user).exists()

        if cart:
            cart = Cart.objects.get(client=self.request.user)
            return render(request, "shop/cart_detail.html", {"cart": cart})

        cart = Cart.objects.create(client=self.request.user)
        return render(request, "shop/cart_detail.html", {"cart": cart})

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user)
        new_order = Order()
        new_order.client = self.request.user
        new_order.status = 1
        new_order.save()

        for el in cart.productcart_set.all():
            new_product_order = ProductOrder()
            new_product_order.product = el.product
            new_product_order.order = new_order
            new_product_order.amount = el.amount
            new_product_order.save()

        new_order.save()
        cart.products.clear()

        return redirect("shop:order-detail", pk=new_order.pk)


class CartProductDeleteView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user)
        product = cart.productcart_set.get(product_id=kwargs.get("pk"))
        return render(
            request, "shop/cart_product_confirm_delete.html", {"product": product}
        )

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user)
        product = cart.productcart_set.get(product_id=kwargs.get("pk"))
        product.delete()
        return redirect("shop:cart-detail")


class OrderListView(ListView):
    model = Order
    template_name = "shop/order_list.html"
    context_object_name = "orders"

    def get_queryset(self) -> QuerySet:
        return Order.objects.filter(client=self.request.user)


class OrderDetailView(DetailView):
    model = Order
    template_name = "shop/order_detail.html"


class ShopProductAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "shop.add_availability"

    def get(self, request, *args, **kwargs):
        form = ShopProductAddForm()
        return render(request, "shop/shop_product_add_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ShopProductAddForm(request.POST)
        shop = Shop.objects.get(pk=self.kwargs.get("pk"))
        if form.is_valid():

            if shop.availability_set.filter(
                product_id=form.cleaned_data["product"]
            ).exists():
                available = shop.availability_set.get(
                    product_id=form.cleaned_data["product"]
                )
                available.amount += form.cleaned_data["amount"]
                available.save()
            else:
                available = Availability()
                available.product = Product.objects.get(pk=form.cleaned_data["product"])
                available.shop = shop
                available.amount = form.cleaned_data["amount"]
                available.save()

            shop.save()
            return redirect("shop:shop-detail", pk=shop.pk)
        return render(request, "shop/shop_product_add_form.html", {"form": form})


class ShopProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "shop.delete_availability"

    def get(self, request, *args, **kwargs):
        shop = Shop.objects.get(pk=self.kwargs.get("pk"))
        product = shop.availability_set.get(product_id=self.kwargs.get("product_id"))
        return render(
            request, "shop/shop_product_confirm_delete.html", {"product": product}
        )

    def post(self, request, *args, **kwargs):
        shop = Shop.objects.get(pk=self.kwargs.get("pk"))
        product = shop.availability_set.get(product_id=self.kwargs.get("product_id"))
        product.delete()
        return redirect("shop:shop-detail", pk=shop.pk)
