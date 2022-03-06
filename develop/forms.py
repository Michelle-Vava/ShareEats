# class SellerInfoForm(forms.Form):
#     firstname = forms.CharField(max_length=20)
#     lastname = forms.CharField(max_length=20)
# from develop.models import SellerInfoForm
#
# remove phone number_fields

from django import forms
from django.forms import TextInput

# KWEKU WAS HERE
from develop.models import SellerInfo, BuyerInfo, DishInfo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class SellerInfoForm(forms.ModelForm):
    class Meta:
        model = SellerInfo
        fields = [
            "businessname",
            "phone",
            "address",
            "description",
            "cardnumber",
            "cvv",
            "expiry_date",
        ]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "BusinessName",
                }
            ),
            "email": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Email",
                }
            ),
        }


class BuyerInfoForm(forms.ModelForm):
    class Meta:
        model = BuyerInfo
        fields = ["firstname", "lastname", "phone"]


class DishInfoForm(forms.ModelForm):
    class Meta:
        model = DishInfo
        fields = ["item", "price", "quantity", "category", "image"]


class BuyerSettings(forms.ModelForm):
    firstname = forms.CharField(
        label="First Name",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "placeholder": "First Name",
            }
        ),
    )
    lastname = forms.CharField(
        label="Last Name",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "placeholder": "Last Name",
            }
        ),
    )
    phone = forms.CharField(
        label="Phone",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "placeholder": "Phone",
            }
        ),
    )

    class Meta:
        model = BuyerInfo
        fields = ["firstname", "lastname", "phone"]
        
        
class SellerSettings(forms.ModelForm):
    businessname = forms.CharField(
        label="Buisness Name",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "placeholder": "BusinessName",
            }
        ),
    )
    phone = forms.CharField(
        label="Phone",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "placeholder": "Phone",
            }
        ),
    )
    address = forms.CharField(
        label="Address",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "placeholder": "address",
            }
        ),
    )
    description = forms.CharField(
        label="Description",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "placeholder": "description",
            }
        ),
    )
    cardnumber = forms.CharField(
        label="Card Number",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
            }
        ),
    )
    cvv = forms.CharField(
        label="CVV",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
            }
        ),
    )
    expiry_date = forms.CharField(
        label="Exp Date",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "PlaceHolder": "MMYY",
            }
        ),
    )

    class Meta:
        model = SellerInfo
        fields = [
            "businessname",
            "phone",
            "address",
            "description",
            "cardnumber",
            "cvv",
            "expiry_date",
        ]
