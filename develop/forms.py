# class SellerInfo(forms.Form):
#     firstname = forms.CharField(max_length=20)
#     lastname = forms.CharField(max_length=20)

from django import forms
from develop.models import SellerInfo


class SellerInfo(forms.ModelForm):
    class Meta:
        model = SellerInfo
        fields = ['business_name',
         'seller_email',
         'seller_address',
         'seller_phone',
         'company_desc',
         'card_number',
         'exp_month',
         'exp_year',
         'cvv']

# TODO: Buyer Form : Kweku and Vineeth
# Please NOTE : make sure to add migrations


# TODO: Seller Form : Vijay and Shubham