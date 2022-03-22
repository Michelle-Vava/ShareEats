import datetime
import json

import stripe
from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from develop import verify
from develop.forms import (
    BuyerSettings,
    SellerInfoForm,
    BuyerInfoForm,
    DishInfoForm,
    SellerSettings, VerifyForm, UserCreationForm
)
from develop.models import BuyerInfo, SellerInfo, Product, Order, OrderItem

from .forms import searchrestaurant

"""
"""

stripe.api_key = settings.STRIPE_SECRET_KEY


# take user to stripe checkout
def CreateCheckoutSessionView(request):
    order = OrderItem.objects.get(user=request.user, product_id=1)
    YOUR_DOMAIN = "http://127.0.0.1:7000"  # change in production #changes to 8000
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': order.product.stripe_price_id,
                'quantity': order.quantity,
            },
        ],
        mode='payment',
        success_url=YOUR_DOMAIN + '/buyer/orders',
        cancel_url=YOUR_DOMAIN + '/cancel/',
    )
    return redirect(checkout_session.url)


# for canceling the order
class CancelView(TemplateView):
    template_name = "buyer/cancel.html"


# home view
# renders the view for the home page
# landing page which is our login
def home(request):
    return render(request, "registration/login.html")


# ability for user to select buyer or seller option
def buyer_seller_option(request):
    return render(request, "buyer-or-seller-option.html")


# login verification using twilio
def login_verify_code(request):
    verify.send(request.user.phone)
    return redirect('verify')


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
            verify.send(form.cleaned_data.get('phone'))
            login(request, user)
            return HttpResponseRedirect("verify")
        else:
            for msg in form.errors:
                print(form.errors[msg])
            return render(request, "registration/signup.html", {"form": form})
    else:
        form = UserCreationForm
        return render(request, "registration/signup.html", {"form": form})


# verification using Twilio
@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.phone, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('option')
        else:
            form = VerifyForm()
            return render(request, 'twilio/verify.html', {'form': form})
    else:
        form = VerifyForm()
        return render(request, 'twilio/verify.html', {'form': form})


# buyer dashboard
def buyer_dashboard(request):
    dishes = Product.objects.all()
    userdetails = BuyerInfo.objects.get(user=request.user)
    context = {"dishes": dishes, "userdetails": userdetails}
    return render(request, "buyer/buyer_dashboard.html", context)


# seller dashboard page
def seller_dashboard(request):
    user_details = SellerInfo.objects.get(user=request.user)
    context = {"userdetails": user_details}
    return render(request, "seller/seller_dashboard.html", context)


# reports page
def reports(request):
    user_details = SellerInfo.objects.get(user=request.user)
    context = {"userdetails": user_details}
    return render(request, "seller/report.html", context)


# edit menu page
def editmenu(request):
    user_details = SellerInfo.objects.get(user=request.user)
    dishes = Product.objects.filter(user=request.user).order_by("product")

    form = DishInfoForm
    context = {"dishes": dishes, "addform": form, "userdetails": user_details}
    return render(request, "seller/editmenu.html", context)


# seller page settings
def seller_settings(request):
    user_details = SellerInfo.objects.get(user=request.user)

    if request.method != "POST":
        seller = SellerInfo.objects.get(user=request.user)
        businessname = seller.businessname
        phone = seller.phone
        address = seller.address
        description = seller.description
        context = {
            "businessname": businessname,
            "phone": phone,
            "address": address,
            "description": description,
            "userdetails": user_details
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
            seller.membership = True
            seller.save()

            return HttpResponseRedirect("/seller/dashboard")
        else:
            context = {"userdetails": user_details, "form": filled_form}
            return render(request, "seller/seller_settings.html", context)


# order page
def order(request):
    userdetails = BuyerInfo.objects.get(user=request.user)
    time = datetime.datetime.now().timestamp()
    # Todo :  remove OrderItem and complete order in order table
    context = {"userdetails": userdetails, "time": time}
    return render(request, "buyer/order.html", context)


# favourites page
def favourites(request):
    userdetails = BuyerInfo.objects.get(user=request.user)
    context = {"userdetails": userdetails}
    return render(request, "buyer/favourites.html", context)


# buyer form
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
                for msg in filled_form.errors:
                    print(filled_form.errors[msg])
                return render(request, "buyer/buyer_form.html", {"form": filled_form})
        else:
            form = BuyerInfoForm
            return render(request, "buyer/buyer_form.html", {"buyerform": form})


# seller form
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
                seller.membership = True
                seller.save()
                return HttpResponseRedirect("/seller/dashboard")

            else:
                for msg in filled_form.errors:
                    print(filled_form.errors[msg])
                return render(request, "seller/seller_form.html", {"form": filled_form})
        else:
            form = SellerInfoForm
            return render(request, "seller/seller_form.html", {"sellerform": form})


# ability for seller to add item to the edit menu
def add_item(request):
    if request.method == "POST":
        filled_form = DishInfoForm(request.POST, request.FILES)
        if filled_form.is_valid():
            dish = Product()

            # TODO : add price from Price Table
            dish.user = request.user
            dish.price = filled_form.cleaned_data["price"]
            unit_price = int(dish.price) * 100
            dish.product = filled_form.cleaned_data["product"]
            dish.seller = SellerInfo.objects.get(user=request.user)
            dish.image = filled_form.cleaned_data["image"]
            dish.quantity = filled_form.cleaned_data["quantity"]
            dish.category = filled_form.cleaned_data["category"]
            product = stripe.Product.create(name=dish.product, images=[dish.image])
            dish.stripe_product_id = product.id
            stripe_price = stripe.Price.create(
                unit_amount=unit_price,
                currency="cad",
                product=product.id,
            )
            dish.stripe_price_id = stripe_price.id
            dish.save()

            return HttpResponseRedirect("/seller/editmenu")
        else:
            for msg in filled_form.errors:
                print(filled_form.errors[msg])


# add to cart : to use in the future
def add_dish(request):
    return HttpResponseRedirect("/buyer/checkout")


# ability to edit food item on seller page
def edit_item(request):
    return HttpResponseRedirect("/seller/editmenu")


# settings for buyer page
def buyer_settings(request):
    userdetails = BuyerInfo.objects.get(user=request.user)

    if request.method != "POST":
        user_details = BuyerInfo.objects.get(user=request.user)
        firstname = user_details.firstname
        lastname = user_details.lastname
        phone = user_details.phone
        initial = {"firstname": firstname, "lastname": lastname, "phone": phone}
        filled_form = BuyerSettings(initial=initial)
        context = {"userdetails": userdetails, "settings": filled_form}
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
            for msg in filled_form.errors:
                print(filled_form.errors[msg])
                context = {"userdetails": userdetails, "settings": filled_form}
                return render(request, "buyer/buyer_settings.html", context)


# views all the restaurants
def restaurants(request):
    user_details = SellerInfo.objects.all()
    context = {"userdetails": user_details}
    return render(request, "buyer/restaurants.html", context)












# adding item to cart
@csrf_exempt
def add_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    # https://stackoverflow.com/questions/61543829/django-taking-values-from-post-request-javascript-fetch-api

    item = post_data["product"]
    quantity = post_data["quantity"]
    # action = post_data["action"]
    productname = Product.objects.get(product=item)

    orderdetails, created = Order.objects.get_or_create(user=request.user,
                                                        buyer=BuyerInfo.objects.get(user=request.user),
                                                        complete=False)
    orderItem, created = OrderItem.objects.get_or_create(user=request.user, order=orderdetails, product=productname,
                                                         buyer=BuyerInfo.objects.get(user=request.user),
                                                         quantity=quantity
                                                         )
    orderItem.save()

    return JsonResponse({"code": 200})


# deleting item from card
@csrf_exempt
def delete_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    # https://stackoverflow.com/questions/61543829/django-taking-values-from-post-request-javascript-fetch-api

    item_id = post_data["item_id"]
    user_id = request.user

    OrderItem.objects.get(item_id=item_id, user_id=user_id).delete()

    return JsonResponse({"code": 200})


# update item from cart
@csrf_exempt
def modify_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    item_id = post_data["item_id"]
    user_id = request.user.id
    quantity = post_data["quantity"]

    c = OrderItem.objects.get(user_id=user_id, item_id=item_id)
    c.quantity = quantity
    c.save()

    return JsonResponse({"code": 200})


# cart page
def cart(request):
    userdetails = BuyerInfo.objects.get(user=request.user)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, buyer=BuyerInfo.objects.get(user=request.user),
                                                     complete=False)
        items = order.orderitem_set.all()
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order, "userdetails": userdetails}
    return render(request, 'buyer/cart.html', context)


def restaurants(request):
    if request.method != "POST":
        form = searchrestaurant()
        FinalList = SellerInfo.objects.all()
        return render(request, "buyer/restaurants.html", {"form": form, "list": FinalList})
    elif request.method == "POST":
        filledform = searchrestaurant(request.POST)
        if filledform["name"].value() == "" and filledform["loc"].value() == "":
            prelistbyres = SellerInfo.objects.all()
        else:
            prelistbyres = SellerInfo.objects.filter(businessname__icontains = filledform["name"].value(), address__icontains = filledform["loc"].value())
        if filledform["name"].value()!="":
            prelistbydish = Product.objects.filter(product__icontains = filledform["name"].value())

        listbydish = []
        if filledform["name"].value()!="":
            for i in prelistbydish:
                if filledform["loc"].value() in i.seller.address:
                    listbydish.append(i.seller)
        listbyres = []
        for i in prelistbyres:
            listbyres.append(i)
        FinalList = listbyres + listbydish
        FinalList = list(dict.fromkeys(FinalList))

        return render(request, "buyer/restaurants.html", {"form": filledform, "list": FinalList})

