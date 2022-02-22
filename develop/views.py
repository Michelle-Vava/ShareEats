from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

"""
"""


# Create your views here.

# home view
# renders the view for the home page
# landing page which is our login
def home(request):
    return render(request, 'registration/login.html')


def buyer_seller_option(request):
    return render(request, 'buyer-or-seller-option.html')


# log out view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


# sign up view
# sign up for authentication
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('option')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = UserCreationForm
        return render(request, 'registration/signup.html', {'form': form})


# # sign up view for buyer
# def buyer_signup(request):
#     return render(request, 'buyer-sign-up.html')
#
#
# # sign in for buyer
# def buyer_signin(request):
#     return render(request, 'buyer-sign-in.html')

def buyer_dashboard(request):
    return render(request, 'buyer_dashboard.html')

# add more : Shubham and Vijay
def seller_form(request):
    return render(request, 'seller_form.html')

# add more : Kweku and Vineeth
def buyer_form(request):
    return render(request, 'buyer_form.html')

# def buyer_dashboard(request):
#     if request.method == 'POST':
#         filled_form = SellerInfo(request.POST)
#         # filled_form.user = request.username
#         if filled_form.is_valid():
#             note = 'Thanks for creating a seller profile %s.You can proceed to the dashboard' % (
#                 filled_form.cleaned_data['firstname'],)
#             filled_form.save()
#             new_form = SellerInfo()
#             return render(request, 'buyer_dashboard.html', {'sellerform': new_form, 'note': note})
#
#     else:
#         form = SellerInfo()
#     return render(request, 'buyer_dashboard.html', {'sellerform': form})

# TODO : To add all the remain views
