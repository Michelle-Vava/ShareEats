from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.core.validators import RegexValidator

from develop.models import User
from django import forms
from django.forms import TextInput

from develop.models import SellerInfo, BuyerInfo, Product

# Internally, PhoneNumberField is based upon CharField and by' \
# default represents the number as a string of an international phonenumber in the database (e.g '+41524204242').

phone_regex = RegexValidator(regex=r"^\+?1?\d{9,15}$")


class UserCreationForm(BaseUserCreationForm):
    phone = forms.CharField(
        max_length=20,
        validators=[phone_regex],
        required=True,
        help_text="Phone number must be entered in the format: "
        "+999999999. Up to 15 digits is allowed.",
    )

    class Meta:
        model = User
        fields = ("username", "phone", "email", "password1", "password2")


class SellerInfoForm(forms.ModelForm):
    business_phone_number = forms.CharField(
        max_length=20,
        validators=[phone_regex],
        required=True,
        help_text="Phone number must be entered in the format: "
        "+999999999. Up to 15 digits is allowed.",
    )
    description = forms.CharField(
        widget=forms.Textarea, help_text="Enter the description of the business"
    )
    address = forms.CharField(help_text="Enter the address of the business/house")

    class Meta:
        model = SellerInfo
        fields = [
            "businessname",
            "business_phone_number",
            "address",
            "description",
        ]


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True)


class BuyerInfoForm(forms.ModelForm):
    class Meta:
        model = BuyerInfo
        fields = ["firstname", "lastname"]


class DishInfoForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product", "servings", "price", "category", "image"]


class EditDishInfoForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product", "servings", "price", "category", "image"]

    def __init__(self, *args, **kwargs):
        super(EditDishInfoForm, self).__init__(*args, **kwargs)
        self.fields["image"].required = False


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

    class Meta:
        model = BuyerInfo
        fields = ["firstname", "lastname"]


class SellerSettings(forms.ModelForm):
    businessname = forms.CharField(
        label="Business Name",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 300px;",
                "placeholder": "BusinessName",
            }
        ),
    )
    business_phone_number = forms.CharField(
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
        fields = ["businessname", "business_phone_number", "address", "description"]


class searching_restaurants(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Restaurants or Dishes"}),
        required=False,
        label="",
    )
    loc = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Location"}),
        required=False,
        label="",
    )
