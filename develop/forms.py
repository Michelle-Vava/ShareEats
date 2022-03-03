# class SellerInfoForm(forms.Form):
#     firstname = forms.CharField(max_length=20)
#     lastname = forms.CharField(max_length=20)
# from develop.models import SellerInfoForm
#
#
from django import forms
from django.forms import TextInput
# KWEKU WAS HERE
from develop.models import SellerInfo, BuyerInfo, DishInfo


class SellerInfoForm(forms.ModelForm):
    class Meta:
        model = SellerInfo
        fields = ['businessname', 'phone', 'address', 'description', 'cardnumber', 'Cvv', 'ExpiryDate']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'BusinessName'
            }),
            'email': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Phone'
            })
        }


class BuyerInfoForm(forms.ModelForm):
    class Meta:
        model = BuyerInfo
        fields = ['firstname', 'lastname', 'phone']


class DishInfoForm(forms.ModelForm):
    class Meta:
        model = DishInfo
        fields = ['item', 'price', 'quantity', 'category', 'image']
