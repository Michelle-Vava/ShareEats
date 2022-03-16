import json

import stripe
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
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
from develop.models import BuyerInfo, SellerInfo, DishInfo, Price, User, CartItem, Order, OrderItem

"""
"""
# TWILIO_ACCOUNT_SID = "ACf91579ced56697582b00416541947683"
# TWILIO_AUTH_TOKEN = "9a2f8474b329324195b3ec3432f23eba"


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(user_id=request.user)
        YOUR_DOMAIN = "http://127.0.0.1:7000"  # change in production
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    # TODO: change quantity t get from Dish table
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


# TESTING STRIPE
class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = DishInfo.objects.get(product="Test Product", user_id=1)
        prices = Price.objects.filter(product=product)
        context = super(ProductLandingPageView,
                        self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices,

        })
        return context


# home view
# renders the view for the home page
# landing page which is our login
def home(request):
    return render(request, "registration/login.html")


def buyer_seller_option(request):
    return render(request, "buyer-or-seller-option.html")


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
            return render(request, 'verify.html', {'form': form})
    else:
        form = VerifyForm()
        return render(request, 'verify.html', {'form': form})


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
    dishes = DishInfo.objects.filter(user=request.user).order_by("product")

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
    data = []
    products = CartItem.objects.filter(user_id=request.user)
    price = 0

    for i in products:
        item = DishInfo.objects.get(product=i.product)
        # pic = DishInfo.objects.filter(.id)[0]
        data.append([item, i])
        print(i.quantity)
        # item.price
        price += (3 * i.quantity)

    context = {"userdetails": userdetails, "data": data,
               "price": '%.2f' % round(price, 2)}
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
                for msg in filled_form.errors:
                    print(filled_form.errors[msg])
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


def add_item(request):
    if request.method == "POST":
        filled_form = DishInfoForm(request.POST, request.FILES)
        if filled_form.is_valid():
            dish = DishInfo()
            price_model = Price()
            # TODO : add price from Price Table
            dish.user = request.user
            price_model.price = 4  # filled_form.cleaned_data["price"]

            dish.product = filled_form.cleaned_data["product"]
            dish.seller = SellerInfo.objects.get(user=request.user)
            dish.image = filled_form.cleaned_data["image"]
            dish.quantity = filled_form.cleaned_data["quantity"]
            dish.category = filled_form.cleaned_data["category"]
            product = stripe.Product.create(name=dish.product)
            dish.stripe_product_id = product.id
            stripe_price = stripe.Price.create(
                unit_amount=price_model.price,
                currency="cad",
                recurring={"interval": "month"},
                product=product.id,
            )

            dish.save()
            price_model.stripe_price_id = stripe_price.id
            price_model.seller = SellerInfo.objects.get(user=request.user)
            price_model.user = request.user
            price_model.product = dish
            price_model.save()
            # add item to stripe

            return HttpResponseRedirect("/seller/editmenu")
        else:
            for msg in filled_form.errors:
                print(filled_form.errors[msg])


def add_dish(request):
    return HttpResponseRedirect("/buyer/checkout")


def edit_item(request):
    return HttpResponseRedirect("/seller/editmenu")


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


def restaurants(request):
    user_details = SellerInfo.objects.all()
    context = {"userdetails": user_details}
    return render(request, "buyer/restaurants.html", context)


@csrf_exempt
def add_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    # https://stackoverflow.com/questions/61543829/django-taking-values-from-post-request-javascript-fetch-api

    item = post_data["product"]
    quantity = post_data["quantity"]
    user_id = request.user
    buyerdetails = BuyerInfo.objects.get(user=request.user)
    CartItem(product=item, user=user_id, quantity=quantity, buyer=buyerdetails).save()

    return JsonResponse({"code": 200})


@csrf_exempt
def delete_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    # https://stackoverflow.com/questions/61543829/django-taking-values-from-post-request-javascript-fetch-api

    item_id = post_data["item_id"]
    user_id = request.user
    # buyerdetails = BuyerInfo.objects.get(user=request.user)

    CartItem.objects.get(item_id=item_id, user_id=user_id).delete()

    return JsonResponse({"code": 200})


@csrf_exempt
def modify_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    item_id = post_data["item_id"]
    user_id = request.user.id
    quantity = post_data["quantity"]

    c = CartItem.objects.get(user_id=user_id, item_id=item_id)
    c.quantity = quantity
    c.save()

    return JsonResponse({"code": 200})


def calculate_order_amount(items):
    """
        items: [["item-id", quantity]]
    """
    price = 0
    items = list(items)

    for i in items:
        item = DishInfo.objects.get(id=i[0])
        price += float(item.price) * float(i[1])

    return int(price * 100)


def get_all_cart_item(request):
    if request.GET.get("item_id") == '' or request.GET.get("item_id") is None:
        items = CartItem.objects.filter(user_id=request.user.id)
        data = [[i.item_id, i.quantity] for i in items]

    else:
        item_id = request.GET["item_id"]
        quantity = request.GET["quantity"]
        data = [[item_id, quantity]]

    return JsonResponse({"purchase": data})
