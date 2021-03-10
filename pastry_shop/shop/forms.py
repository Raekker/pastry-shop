from django import forms

from pastry_shop.shop.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {"categories": forms.CheckboxSelectMultiple}
