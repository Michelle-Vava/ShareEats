from django import forms

# class SellerInfo(forms.Form):
#     firstname = forms.CharField(max_length=20)
#     lastname = forms.CharField(max_length=20)
from develop.models import SellerInfo


class SellerInfo(forms.ModelForm):
    class Meta:
        model = SellerInfo
        fields = ['firstname', 'lastname']
