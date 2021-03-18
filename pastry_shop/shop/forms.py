from django import forms

from pastry_shop.shop.models import Product, ProductCart


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {"categories": forms.CheckboxSelectMultiple}


class CartProductAddForm(forms.Form):
    amount = forms.IntegerField(min_value=1)


class ShopProductAddForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    amount = forms.IntegerField()
