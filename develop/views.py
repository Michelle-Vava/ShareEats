from urllib import request
from wsgiref.util import request_uri
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from develop.forms import BuyerSettings, SellerInfoForm, BuyerInfoForm, DishInfoForm
from develop.models import BuyerInfo, SellerInfo, DishInfo

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


def buyer_dashboard(request):
    dishes = DishInfo.objects.all()
    userdetails = BuyerInfo.objects.get(user=request.user)
    context = {'dishes': dishes, 'userdetails': userdetails}
    return render(request, 'buyer/buyer_dashboard.html', context)


def seller_dashboard(request):
    userdetails = SellerInfo.objects.get(user=request.user)
    context = {'userdetails': userdetails}
    return render(request, 'seller/seller_dashboard.html', context)


def reports(request):
    return render(request, 'seller/report.html')


def editmenu(request):
    dishes = DishInfo.objects.filter(user=request.user).order_by('item')

    form = DishInfoForm
    context = {'dishes': dishes, 'addform': form}
    return render(request, 'seller/editmenu.html', context)




def seller_settings(request):
    return render(request, 'seller/seller_settings.html')


def order(request):
    return render(request, 'buyer/order.html')


def favourites(request):
    return render(request, 'buyer/favourites.html')


def checkout(request):
    return render(request, 'buyer/checkout.html')


def buyer_form(request):
    if BuyerInfo.objects.filter(user=request.user, membership=True).exists():
        return HttpResponseRedirect('/buyer/dashboard')
    else:
        if request.method == 'POST':
            filled_form = BuyerInfoForm(request.POST)
            if filled_form.is_valid():
                buyer = BuyerInfo()
                buyer.user = request.user
                buyer.firstname = filled_form.cleaned_data['firstname']
                buyer.lastname = filled_form.cleaned_data['lastname']
                buyer.membership = True
                buyer.save()
                return HttpResponseRedirect('buyer/buyer_dashboard.html')
            else:
                for msg in filled_form.error_messages:
                    print(filled_form.error_messages[msg])
                return render(request, 'buyer/buyer_form.html', {'form': filled_form})
        else:
            form = BuyerInfoForm
            return render(request, 'buyer/buyer_form.html', {'buyerform': form})


def seller_form(request):
    if SellerInfo.objects.filter(user=request.user, membership=True).exists():
        return HttpResponseRedirect('/seller/dashboard')
    else:
        if request.method == 'POST':
            filled_form = SellerInfoForm(request.POST)
            if filled_form.is_valid():
                seller = SellerInfo()
                seller.user = request.user
                seller.businessname = filled_form.cleaned_data['businessname']
                seller.phone = filled_form.cleaned_data['phone']
                seller.address = filled_form.cleaned_data['address']
                seller.description = filled_form.cleaned_data['description']
                seller.cardnumber = filled_form.cleaned_data['cardnumber']
                seller.Cvv = filled_form.cleaned_data['Cvv']
                seller.ExpiryDate = filled_form.cleaned_data['ExpiryDate']
                seller.membership = True
                seller.save()
                return HttpResponseRedirect('/seller/dashboard')

            else:
                for msg in filled_form.error_messages:
                    print(filled_form.error_messages[msg])
                return render(request, 'seller/seller_form.html', {'form': filled_form})
        else:
            form = SellerInfoForm
            return render(request, 'seller/seller_form.html', {'sellerform': form})


def add_item(request):
    if request.method == 'POST':
        filled_form = DishInfoForm(request.POST, request.FILES)
        if filled_form.is_valid():
            dish = DishInfo()
            dish.user = request.user
            dish.price = filled_form.cleaned_data['price']
            dish.item = filled_form.cleaned_data['item']
            dish.seller_id = SellerInfo.objects.get(user=request.user)
            dish.image = filled_form.cleaned_data['image']
            dish.quantity = filled_form.cleaned_data['quantity']
            dish.category = filled_form.cleaned_data['category']
            dish.save()
            return HttpResponseRedirect('/seller/editmenu')
        else:
            for msg in filled_form.error_messages:
                print(filled_form.error_messages[msg])


def buyer_settings(request):
    if request.method == "POST":
        filled_form = BuyerSettings(request.POST, request.FILES)
        if filled_form.is_valid():
            
            buyer = BuyerInfo()
            buyer.user = request.user
            buyer.id = request.user.pk
            buyer.firstname = filled_form.cleaned_data['firstname']
            buyer.lastname = filled_form.cleaned_data['lastname']
            buyer.membership = True
            buyer.save()
            
            return HttpResponseRedirect('dashboard')            
    
    else:
        user_details = BuyerInfo.objects.get(user=request.user)        
        filled_form = BuyerSettings()
        filled_form.firstname = user_details.firstname
        filled_form.lastname = user_details.lastname
        filled_form.phone = user_details.phone
        return render(request, 'buyer/buyer_settings.html',{'settings': filled_form})
    # if filled_form.is_valid():
    #     buyer = BuyerInfo()
    #     buyer.firstname = BuyerInfo.firstname.objects.get(user=request.user)
    #     buyer.lastname = BuyerInfo.lastname.objects.get(user=request.user)
    #     buyer.phone = BuyerInfo.phone.objects.get(user=request_user)
    #     return HttpResponseRedirect('/buyer/settings')

        
        

        