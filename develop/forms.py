from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.forms import TextInput
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from develop.models import SellerInfo, BuyerInfo, Product
from develop.models import User


# Internally, PhoneNumberField is based upon CharField and by' \
# default represents the number as a string of an international phonenumber in the database (e.g '+41524204242').

# phone_regex = RegexValidator(regex=r"^\+?1?\d{9,15}$")


class UserCreationForm(BaseUserCreationForm):
    phone = PhoneNumberField(
        max_length=15,
        widget=PhoneNumberPrefixWidget(initial='CA'),
        required=True,
        help_text="Enter your 10 digit phone number",

    )

    class Meta:
        model = User
        fields = ("username", "phone", "email", "password1", "password2")


class SellerInfoForm(forms.ModelForm):
    business_phone_number = PhoneNumberField(
        max_length=15,
        # validators=[phone_regex],
        widget=PhoneNumberPrefixWidget(initial="CA"),
        required=True,
        help_text="Enter your 10 digit phone number",

    )
    description = forms.CharField(
        widget=forms.Textarea, help_text="Enter the description of the business"
    )
    address = forms.CharField(help_text="Enter the address of the business/house")
    image = forms.ImageField(help_text="Optional.", required=False)

    class Meta:
        model = SellerInfo
        fields = [
            "businessname",
            "business_phone_number",
            "address",
            "description",
            "image",
        ]


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=6, required=True)


class BuyerInfoForm(forms.ModelForm):
    class Meta:
        model = BuyerInfo
        fields = ["firstname", "lastname"]


class DishInfoForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product", "servings", "price", "category", "image"]


class EditDishInfoForm(forms.ModelForm):
    id = forms.IntegerField()

    class Meta:
        model = Product
        fields = ["product", "servings", "price", "category", "availability", "image"]

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput

        super(EditDishInfoForm, self).__init__(*args, **kwargs)
        self.fields["image"].required = False
        self.fields["id"].widget = HiddenInput()


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
    business_phone_number = PhoneNumberField(
        max_length=15,
        # validators=[phone_regex],
        widget=PhoneNumberPrefixWidget(initial='CA'),
        required=True,
        help_text="Enter your 10 digit phone number",

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
    image = forms.ImageField(help_text="Optional.", required=False)

    class Meta:
        model = SellerInfo
        fields = ["businessname", "business_phone_number", "address", "description", "image"]


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


class searching_dishes(forms.Form):
    dishname = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'Dish Name'}), required=False, label='')
    category = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'Category'}), required=False, label='')
