# class SellerInfo(forms.Form):
#     firstname = forms.CharField(max_length=20)
#     lastname = forms.CharField(max_length=20)
# from develop.models import SellerInfo
#
#
from django import forms

from develop.models import SellerInfo, BuyerInfo


class SellerInfo(forms.ModelForm):
    class Meta:
        model = SellerInfo
        fields = ['businessname', 'phone', 'address', 'description', 'cardnumber', 'Cvv', 'ExpiryDate']


class BuyerInfo(forms.ModelForm):
    class Meta:
        model = BuyerInfo
        fields = ['firstname', 'lastname', 'phone']
