from django import forms
from product.models import (Order,
                            OrderItem,
                            Promocode,
                            Product,
                            PresentationImages)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'currency', 'rate_currency',
        'promo', 'delivery_method',]


class ChangeStatusOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status',]


class CreatePromo(forms.ModelForm):
    class Meta:
        model = Promocode
        fields = ['code', 'type_code', 'amount_of_discount', 'type_promo', 'status', 'start_promo', 'end_promo']


class ProductImage(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['photo']


class PresentationImageForm(forms.ModelForm):
    class Meta:
        model = PresentationImages
        fields = '__all__'
