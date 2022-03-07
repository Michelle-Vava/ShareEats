from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from develop.forms import (
    BuyerSettings,
    SellerInfoForm,
    BuyerInfoForm,
    DishInfoForm,
    SellerSettings,
)
from develop.models import BuyerInfo, SellerInfo, DishInfo

"""
"""


# Create your views here.

# home view
# renders the view for the home page
# landing page which is our login
def home(request):
    return render(request, "registration/login.html")


def buyer_seller_option(request):
    return render(request, "buyer-or-seller-option.html")


# log out view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


# sign up view
# sign up for authentication
def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("option")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request, "registration/signup.html", {"form": form})
    else:
        form = UserCreationForm
        return render(request, "registration/signup.html", {"form": form})


def buyer_dashboard(request):
    dishes = DishInfo.objects.all()
    userdetails = BuyerInfo.objects.get(user=request.user)
    context = {"dishes": dishes, "userdetails": userdetails}
    return render(request, "buyer/buyer_dashboard.html", context)


def seller_dashboard(request):
    user_details = SellerInfo.objects.get(user=request.user)
    context = {"userdetails": user_details}
    return render(request, "seller/seller_dashboard.html", context)


def reports(request):
    user_details = SellerInfo.objects.get(user=request.user)
    context = {"userdetails": user_details}
    return render(request, "seller/report.html", context)


def editmenu(request):
    user_details = SellerInfo.objects.get(user=request.user)
    dishes = DishInfo.objects.filter(user=request.user).order_by("item")

    form = DishInfoForm
    context = {"dishes": dishes, "addform": form, "userdetails": user_details}
    return render(request, "seller/editmenu.html", context)


def seller_settings(request):
    user_details = SellerInfo.objects.get(user=request.user)

    if request.method != "POST":
        seller = SellerInfo.objects.get(user=request.user)
        businessname = seller.businessname
        phone = seller.phone
        address = seller.address
        description = seller.description
        cardnumber = seller.cardnumber
        cvv = seller.cvv
        expiry_date = seller.expiry_date
        context = {
            "businessname": businessname,
            "phone": phone,
            "address": address,
            "description": description,
            "cardnumber": cardnumber,
            "cvv": cvv,
            "expiry_date": expiry_date, "userdetails": user_details
        }

        form = SellerSettings(initial=context)
        context = {"userdetails": user_details, "form": form}
        return render(request, "seller/seller_settings.html", context)


    else:
        filled_form = SellerSettings(request.POST)
        if filled_form.is_valid():
            seller = SellerInfo()
            seller.user = request.user
            seller.id = SellerInfo.objects.get(user=request.user).id
            seller.businessname = filled_form.cleaned_data["businessname"]
            seller.phone = filled_form.cleaned_data["phone"]
            seller.address = filled_form.cleaned_data["address"]
            seller.description = filled_form.cleaned_data["description"]
            seller.cardnumber = filled_form.cleaned_data["cardnumber"]
            seller.cvv = filled_form.cleaned_data["cvv"]
            seller.expiry_date = filled_form.cleaned_data["expiry_date"]
            seller.membership = True
            seller.save()

            return HttpResponseRedirect("/seller/dashboard")
        else:
            context = {"userdetails": user_details, "form": filled_form}
            return render(request, "seller/seller_settings.html",context)


def order(request):
    userdetails = BuyerInfo.objects.get(user=request.user)
    context = {"userdetails": userdetails}
    return render(request, "buyer/order.html", context)


def favourites(request):
    userdetails = BuyerInfo.objects.get(user=request.user)
    context = {"userdetails": userdetails}
    return render(request, "buyer/favourites.html", context)


def checkout(request):
    userdetails = BuyerInfo.objects.get(user=request.user)
    context = {"userdetails": userdetails}
    return render(request, "buyer/checkout.html", context)


def buyer_form(request):
    if BuyerInfo.objects.filter(user=request.user, membership=True).exists():
        return HttpResponseRedirect("/buyer/dashboard")
    else:
        if request.method == "POST":
            filled_form = BuyerInfoForm(request.POST)
            if filled_form.is_valid():
                buyer = BuyerInfo()
                buyer.user = request.user
                buyer.firstname = filled_form.cleaned_data["firstname"]
                buyer.lastname = filled_form.cleaned_data["lastname"]
                buyer.membership = True
                buyer.save()
                return HttpResponseRedirect("/buyer/dashboard")
            else:
                for msg in filled_form.error_messages:
                    print(filled_form.error_messages[msg])
                return render(request, "buyer/buyer_form.html", {"form": filled_form})
        else:
            form = BuyerInfoForm
            return render(request, "buyer/buyer_form.html", {"buyerform": form})


def seller_form(request):
    if SellerInfo.objects.filter(user=request.user, membership=True).exists():
        return HttpResponseRedirect("/seller/dashboard")
    else:
        if request.method == "POST":
            filled_form = SellerInfoForm(request.POST)
            if filled_form.is_valid():
                seller = SellerInfo()
                seller.user = request.user
                seller.businessname = filled_form.cleaned_data["businessname"]
                seller.phone = filled_form.cleaned_data["phone"]
                seller.address = filled_form.cleaned_data["address"]
                seller.description = filled_form.cleaned_data["description"]
                seller.cardnumber = filled_form.cleaned_data["cardnumber"]
                seller.cvv = filled_form.cleaned_data["cvv"]
                seller.expiry_date = filled_form.cleaned_data["expiry_date"]
                seller.membership = True
                seller.save()
                return HttpResponseRedirect("/seller/dashboard")

            else:
                for msg in filled_form.error_messages:
                    print(filled_form.error_messages[msg])
                return render(request, "seller/seller_form.html", {"form": filled_form})
        else:
            form = SellerInfoForm
            return render(request, "seller/seller_form.html", {"sellerform": form})


def add_item(request):
    if request.method == "POST":
        filled_form = DishInfoForm(request.POST, request.FILES)
        if filled_form.is_valid():
            dish = DishInfo()
            dish.user = request.user
            dish.price = filled_form.cleaned_data["price"]
            dish.item = filled_form.cleaned_data["item"]
            dish.seller_id = SellerInfo.objects.get(user=request.user)
            dish.image = filled_form.cleaned_data["image"]
            dish.quantity = filled_form.cleaned_data["quantity"]
            dish.category = filled_form.cleaned_data["category"]
            dish.save()
            return HttpResponseRedirect("/seller/editmenu")
        else:
            for msg in filled_form.error_messages:
                print(filled_form.error_messages[msg])


def buyer_settings(request):
    userdetails = BuyerInfo.objects.get(user=request.user)

    if request.method != "POST":
        user_details = BuyerInfo.objects.get(user=request.user)
        firstname = user_details.firstname
        lastname = user_details.lastname
        phone = user_details.phone
        initial = {"firstname": firstname, "lastname": lastname, "phone": phone}
        filled_form = BuyerSettings(initial=initial)
        context = {"userdetails": userdetails,"settings": filled_form}
        return render(request, "buyer/buyer_settings.html", context)

    else:
        filled_form = BuyerSettings(request.POST)
        if filled_form.is_valid():
            buyer = BuyerInfo()
            buyer.user = request.user
            buyer.id = BuyerInfo.objects.get(user=request.user).id
            buyer.firstname = filled_form.cleaned_data["firstname"]
            buyer.lastname = filled_form.cleaned_data["lastname"]
            buyer.phone = filled_form.cleaned_data["phone"]
            buyer.membership = True
            buyer.save()
            return HttpResponseRedirect("dashboard")
        else:
            for msg in filled_form.error_messages:
                print(filled_form.error_messages[msg])
                context = {"userdetails": userdetails, "settings": filled_form}
                return render(request, "buyer/buyer_settings.html", context)
def restaurants(request):
    if request.method!="POST":
        context = {""}
        return render(request, "buyer/restuarants.html", context)