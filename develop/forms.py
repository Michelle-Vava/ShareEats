from django import forms

# class SellerInfo(forms.Form):
#     firstname = forms.CharField(max_length=20)
#     lastname = forms.CharField(max_length=20)
# from develop.models import SellerInfo
#
#
# class SellerInfo(forms.ModelForm):
#     class Meta:
#         model = SellerInfo
#         fields = ['firstname', 'lastname']
# TODO: Buyer Form : Kweku and Vineeth
# Please NOTE : make sure to add migrations
class BuyerSignUpForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(
        max_length=17, blank=True
    )  # validators should be a list
    user_name = forms.CharField(max_length=100)


# TODO: Seller Form : Vijay and Shubham
# Hi i was also here, Kweku
