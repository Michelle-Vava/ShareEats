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


class BuyerSettings(forms.ModelForm):
    class Meta:
        model = BuyerInfo
        fields = ['firstname', 'lastname', 'phone']
        widgets = {
            'firstname': TextInput(attrs={
                'placeholder': 'firstname'
            }),
            'lastname': TextInput(attrs={
                'placeholder': 'lastname'
            }),
            'phone': TextInput(attrs={
                'placeholder': 'phone'
            }),
        }
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_id = 'id-exampleForm'
                self.helper.form_class = 'blueForms'
                self.helper.form_method = 'post'
                self.helper.form_action = 'submit_survey'

                self.helper.add_input(Submit('submit', 'Submit'))