from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User
from django import forms
from django.forms import TextInput

from develop.models import SellerInfo, BuyerInfo, DishInfo


class UserCreationForm(BaseUserCreationForm):
    phone = forms.CharField(max_length=20, required=True, help_text='Phone number')

    class Meta:
        model = User
        fields = ('username', 'phone', 'password1', 'password2')


class SellerInfoForm(forms.ModelForm):
    class Meta:
        model = SellerInfo
        fields = [
            "businessname",
            "phone",
            "address",
            "description",
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


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True)


class BuyerInfoForm(forms.ModelForm):
    class Meta:
        model = BuyerInfo
        fields = ["firstname", "lastname", "phone"]


class DishInfoForm(forms.ModelForm):
    class Meta:
        model = DishInfo
        fields = ["product", "quantity", "category", "image"]


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

    class Meta:
        model = SellerInfo
        fields = [
            "businessname",
            "phone",
            "address",
            "description"
        ]
