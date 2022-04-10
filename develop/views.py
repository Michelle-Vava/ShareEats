import datetime
import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from develop.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.db.models import Q
from django.db import transaction
from develop import verify
from develop.forms import (
    BuyerSettings,
    SellerInfoForm,
    BuyerInfoForm,
    DishInfoForm,
    SellerSettings,
    VerifyForm,
    UserCreationForm,
    EditDishInfoForm,
)
from develop.models import BuyerInfo, SellerInfo, Product, Order, Cart, Purchase
from .forms import searching_restaurants, searching_dishes
from .verify import send_message_to_seller, send_message_to_buyer

"""
"""

stripe.api_key = settings.STRIPE_SECRET_KEY


# take user to stripe checkout
def CreateCheckoutSessionView(request):
    order = Cart.objects.filter(user=request.user)
    if order:
        line_items_list = []
        for i in order:
            line_items_list.append(
                {"price": i.product.stripe_price_id, "quantity": i.quantity}
            )
        YOUR_DOMAIN = "http://127.0.0.1:8000"  # change in production #changes to 8000
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items_list,
            mode="payment",
            success_url=YOUR_DOMAIN + "/success/",
            cancel_url=YOUR_DOMAIN + "/cancel/", )
        return redirect(checkout_session.url)
    else:
        return redirect("cart")


# for canceling the order
class CancelView(TemplateView):
    template_name = "buyer/Order/cancel.html"


# for successful the order
def Success(request):
    userdetails = BuyerInfo.objects.get(user=request.user)
    date = datetime.datetime.now()
    cart = Cart.objects.filter(order=Order.objects.get(user=request.user, complete=False), user=request.user,
                               buyer=BuyerInfo.objects.get(user=request.user))
    to_seller = cart.first().product.seller.business_phone_number.as_e164
    to_buyer = userdetails.user.phone.as_e164
    send_message_to_seller(to_seller)
    send_message_to_buyer(to_buyer)
    for i in cart:
        Purchase.objects.create(
            quantity=i.quantity,
            seller_price=i.product.price,
            product=i.product,
            order=i.order,
        )
    cart.delete()
    Order.objects.filter(user=request.user, complete=False).update(complete=True)
    if Order.objects.filter(user=request.user, complete=False).exists():
        order = Order.objects.get(user=request.user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]
    context = {"userdetails": userdetails, "date": date, "cartItems": cartItems}
    return render(request, "buyer/Order/success.html", context)


# home view
# renders the view for the home page
# landing page which is our login
def home(request):
    return render(request, "registration/login.html")


# ability for user to select buyer or seller option
def buyer_seller_option(request):
    return render(request, "base_templates/buyer-or-seller-option.html")


# get phone number as string : client.phone.as_e164
# login verification using twilio
def login_verify_code(request):
    verify.send(request.user.phone.as_e164)
    return redirect("verify")


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
            verify.send(form.cleaned_data.get("phone"))
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
    User = request.user
    if request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("code")
            if verify.check(request.user.phone.as_e164, code):
                request.user.is_verified = True
                request.user.save()
                return redirect("option")
            else:
                messages.error(request, "Incorrect Code.Try Again")
                form = VerifyForm()
                context = {"form": form}
            return render(request, "twilio/verify.html", context)

        else:
            form = VerifyForm()
            context = {"form": form}
            return render(request, "twilio/verify.html", context)
    else:
        form = VerifyForm()
        return render(request, "twilio/verify.html", {"form": form})


@login_required
def verify_code_usernamechange(request):
    User = request.user
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.phone.as_e164, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('seller personalsettings')
        else:
            form = VerifyForm()
            context = {'form': form}
            return render(request, 'twilio/verify.html', context)
    else:
        form = VerifyForm()
        return render(request, 'twilio/verify.html', {'form': form})


# buyer dashboard
def buyer_dashboard(request):
    if request.method != "POST":
        dishes = Product.objects.all()
        unfilledform = searching_dishes()
        userdetails = BuyerInfo.objects.get(user=request.user)
        if Order.objects.filter(user=request.user, complete=False).exists():
            order = Order.objects.get(user=request.user, complete=False)
            cartItems = order.get_cart_items
        else:
            order = {"get_cart_total": 0, "get_cart_items": 0}
            cartItems = order["get_cart_items"]

        context = {
            "dishes": dishes,
            "userdetails": userdetails,
            "cartItems": cartItems,
            "form": unfilledform,
        }
        return render(request, "buyer/buyer_dashboard.html", context)
    else:
        filledform = searching_dishes(request.POST)
        if filledform.is_valid():
            print(filledform["dishname"].value(), filledform["category"].value())
            if (
                    filledform["dishname"].value() == ""
                    and filledform["category"].value() == ""
            ):
                disheslist = Product.objects.all()
            else:
                disheslist = Product.objects.filter(
                    product__icontains=filledform["dishname"].value(),
                    category__icontains=filledform["category"].value(),
                )

        userdetails = BuyerInfo.objects.get(user=request.user)
        if Order.objects.filter(user=request.user, complete=False).exists():
            order = Order.objects.get(user=request.user, complete=False)
            cartItems = order.get_cart_items
        else:
            order = {"get_cart_total": 0, "get_cart_items": 0}
            cartItems = order["get_cart_items"]

        context = {
            "dishes": disheslist,
            "userdetails": userdetails,
            "cartItems": cartItems,
            "form": filledform,
        }
        return render(request, "buyer/buyer_dashboard.html", context)


# seller dashboard page
def seller_dashboard(request):
    user_details = SellerInfo.objects.get(
        user=request.user
    )  # seller object for user logged in
    seller_id = user_details.id

    products = Product.objects.filter(
        seller_id=user_details.id
    )  # query set of all product objects with same seller id

    purchase_obj = []
    for productobject in products:
        purchase = Purchase.objects.filter(
            product_id=productobject.id
        ).exclude(order_status="completed")  # all purchase objects with same product ids and is either "seller notified" or "in progress"
        for i in purchase:
            purchase_obj.append(i)
            # only filtering completed purchases
    completed_purchase_obj = []
    for productobject in products:
        purchase = Purchase.objects.filter(
            product_id=productobject.id, order_status="completed"
        )  # all purchase objects with same product ids and are completed
        for i in purchase:
            completed_purchase_obj.append(i)

    order_obj = []
    product_obj = []
    for obj in purchase_obj:
        order_obj.append(Order.objects.get(id=obj.order_id))
        product_obj.append(Product.objects.get(id=obj.product_id))

    buyerinfo_obj = []
    for order in order_obj:
        buyerinfo_obj.append(BuyerInfo.objects.get(id=order.buyer_id))


    # filtering orders by orderid
    order_dict = {}

    for object in purchase_obj:
        id = object.order
        if id in order_dict.keys():
            order_dict[id].append(object)
        else:
            order_dict[id] = [object]
        

    # zip of all list
    all_completed_orders_list = zip(order_obj, buyerinfo_obj, completed_purchase_obj, product_obj)
    all_list = zip(order_obj, buyerinfo_obj, purchase_obj, product_obj)
    context = {
        "userdetails"   : user_details,
        "purchase"      : purchase_obj,
        "products"      : products,
        "orders"        : order_obj,
        "buyerinfo"     : buyerinfo_obj,
        "all"           : all_list,
        "all_completed" : all_completed_orders_list,
        "order_dict"    : order_dict
    }
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
    edit_form = EditDishInfoForm
    context = {
        "dishes": dishes,
        "addform": form,
        "editform": edit_form,
        "userdetails": user_details,
    }
    return render(request, "seller/editmenu.html", context)


# remove item from edit menu page
def delete_food_item(request, id):
    user_details = SellerInfo.objects.get(user=request.user)
    try:
        Product.objects.get(user=user_details.user, id=id).delete()
    except:
        return HttpResponseRedirect("/seller/editmenu")

    # get 'token' from the session
    # Product.objects.get(product=token).delete()
    return HttpResponseRedirect("/seller/editmenu")


# edit item on the edit menu page
def item(request):
    stripe_update = False
    if request.method == "POST":
        filled_form = EditDishInfoForm(request.POST, request.FILES)
        filled_form.fields["image"].required = False
        if filled_form.is_valid():
            token = filled_form.cleaned_data["id"]
            dish = Product.objects.get(Q(user=request.user), Q(id=token))

            if dish.product != filled_form.cleaned_data["product"]:
                dish.product = filled_form.cleaned_data["product"]
                stripe_update = True
            dish.seller = SellerInfo.objects.get(user=request.user)
            if filled_form.cleaned_data["image"]:
                dish.image = filled_form.cleaned_data["image"]
                stripe_update = True
            dish.servings = filled_form.cleaned_data["servings"]
            dish.category = filled_form.cleaned_data["category"]
            dish.availability = filled_form.cleaned_data["availability"]
            if dish.price != filled_form.cleaned_data["price"]:
                dish.price = filled_form.cleaned_data["price"]
                stripe_update = True

            if stripe_update:
                product = stripe.Product.modify(
                    dish.stripe_product_id, name=dish.product, images=[dish.image]
                )
                # activate new price
                unit_price = float(dish.price) * 100
                stripe_price = stripe.Price.create(
                    unit_amount=int(unit_price),
                    currency="cad",
                    product=product.id,
                    transfer_lookup_key=True,
                )
                dish.stripe_price_id = stripe_price.id

            dish.save()

            return HttpResponseRedirect("/seller/editmenu")
        else:
            for msg in filled_form.errors:
                print(filled_form.errors[msg])


# seller page settings
def seller_settings(request):
    user_details = SellerInfo.objects.get(user=request.user)

    if request.method != "POST":
        seller = SellerInfo.objects.get(user=request.user)
        businessname = seller.businessname
        phone = seller.business_phone_number
        address = seller.address
        description = seller.description
        image = seller.image
        context = {
            "businessname": businessname,
            "business_phone_number": phone,
            "address": address,
            "description": description,
            "userdetails": user_details,
            "image": image,
        }

        form = SellerSettings(initial=context)
        context = {"userdetails": user_details, "form": form}
        return render(request, "seller/seller_settings.html", context)

    else:
        filled_form = SellerSettings(request.POST, request.FILES)
        if filled_form.is_valid():
            seller = SellerInfo()
            seller.user = request.user
            seller.id = SellerInfo.objects.get(user=request.user).id
            seller.businessname = filled_form.cleaned_data["businessname"]
            seller.business_phone_number = filled_form.cleaned_data[
                "business_phone_number"
            ]
            seller.address = filled_form.cleaned_data["address"]
            seller.description = filled_form.cleaned_data["description"]

            if filled_form.cleaned_data["image"] is None:
                seller_current = SellerInfo.objects.get(user=request.user)
                seller.image = seller_current.image
            else:
                seller.image = filled_form.cleaned_data["image"]
            seller.membership = True
            seller.save()
            seller = SellerInfo.objects.get(user=request.user)
            if seller.image == 'False':
                seller = SellerInfo.objects.get(user=request.user)
                seller.image = None
                seller.save()

            return HttpResponseRedirect("/seller/dashboard")
        else:
            context = {"userdetails": user_details, "form": filled_form}
            return render(request, "seller/seller_settings.html", context)


# seller page personalsettings
def seller_personalsettings(request):
    old_user = request.user
    user_details = SellerInfo.objects.get(user=request.user)

    if request.method != "POST":
        user_logindetails = User.objects.get(username=request.user)
        username = user_logindetails.username
        email = user_logindetails.email
        phone = user_logindetails.phone

        context = {
            "username": username,
            "email": email,
            "phone": phone,
            "userdetails": user_logindetails
        }
        form = UserCreationForm(initial=context)
        context = {"userdetails": user_details, "form": form}
        return render(request, "seller/seller_personalsettings.html", context)

    else:
        filled_form = UserCreationForm(request.POST)
        if filled_form.is_valid():
            user = filled_form.save()
            verify.send(filled_form.cleaned_data.get('phone'))
            login(request, user)
            SellerInfo_obj = SellerInfo.objects.get(user=old_user)
            List = Product.objects.filter(seller=SellerInfo_obj)
            for product in List:
                product.user = user
                product.save()
            SellerInfo_obj.user = user
            SellerInfo_obj.save()
            Buyer_obj = BuyerInfo.objects.get(user=old_user)
            Buyer_obj.user = user
            Buyer_obj.save()
            User.objects.filter(username=old_user.username).delete()
            transaction.commit()
            return redirect('verify change')

        else:
            for msg in filled_form.errors:
                print(filled_form.errors[msg])
            # return render(request, "registration/signup.html", {"form": filled_form})
            form = UserCreationForm(instance=user_details)
            context = {"userdetails": user_details, "form": filled_form}
            return render(request, "seller/seller_personalsettings.html", context)


# order page
def order(request):
    userdetails = BuyerInfo.objects.filter(user=request.user)
    info_dict_current = {}

    current = datetime.datetime.now()
    today = current.day

    all_orders = Order.objects.filter(
        user=request.user,
        buyer=BuyerInfo.objects.get(user=request.user),
        complete=True,
        status=False,
    )

    current_orders = []

    for orders in all_orders:
        current_orders.append(orders)

    # For current orders
    for order_object in current_orders:

        current_productid = []
        purchasequery = Purchase.objects.filter(
            order_id=order_object.id, order_status="seller notified"
        )  # filtered purchase queryset for orderid 8,9,10,11

        current_purchaseobjects = []
        for purchase_object in purchasequery:
            current_purchaseobjects.append(purchase_object)
            current_productid.append(purchase_object.product_id)

        current_productobjects = []

        for j in current_productid:  # [3, 5, 5, 1, 4]
            productobject = Product.objects.get(
                id=j
            )  # filtered queryset list where product id = filtered product ids
            current_productobjects.append(productobject)

        info_dict_current[order_object.id] = zip(
            current_purchaseobjects, current_productobjects
        )

    # For returning 0 items if there are no incomplete orders
    if Order.objects.filter(user=request.user, complete=False).exists():
        order = Order.objects.get(user=request.user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]

    context = {
        "userdetails": userdetails,
        "cartItems": cartItems,
        "info_obj_current": info_dict_current,
        "curr_ord": current_orders,
        "today": today
    }

    return render(request, "buyer/Order/Order History/order.html", context)


def complete_order(request):
    info_dict_complete = {}
    userdetails = BuyerInfo.objects.get(user=request.user)

    all_orders = Order.objects.filter(
        user=request.user,
        buyer=BuyerInfo.objects.get(user=request.user),
        complete=True,
        status=True,
    )

    # For complete orders
    for order_object in all_orders:

        all_productid = []
        purchasequery = Purchase.objects.filter(
            order_id=order_object.id, order_status="completed"
        )  # filtered purchase queryset for orderid 8,9,10,11

        all_purchaseobjects = []
        for purchase_object in purchasequery:
            all_purchaseobjects.append(purchase_object)
            all_productid.append(purchase_object.product_id)

        all_productobjects = []

        for j in all_productid:  # [3, 5, 5, 1, 4]
            productobject = Product.objects.get(
                id=j
            )  # filtered queryset list where product id = filtered product ids
            all_productobjects.append(productobject)

        info_dict_complete[order_object.id] = zip(
            all_purchaseobjects, all_productobjects
        )

        # For returning 0 items if there are no incomplete orders
    if Order.objects.filter(user=request.user, complete=False).exists():
        order = Order.objects.get(user=request.user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]

    context = {
        "userdetails": userdetails,
        "info_obj_complete": info_dict_complete,
        "cartItems": cartItems,
    }
    return render(request, "buyer/Order/Order History/completed_order.html", context)


def incomplete_order(request):
    info_dict_incomplete = {}
    userdetails = BuyerInfo.objects.get(user=request.user)
    incomplete_orders = Order.objects.filter(
        user=request.user,
        buyer=BuyerInfo.objects.get(user=request.user),
        complete=False,
    )
    # For incomplete orders
    for order_object in incomplete_orders:

        productId = (
            []
        )  # product id where foreign key of order matches in product entity
        cartquery = Cart.objects.filter(
            order_id=order_object.id
        )  # filtered purchase queryset for orderid 12

        cartobjects = []  # query objects for purchase entity
        for cart_object in cartquery:
            cartobjects.append(cart_object)
            # orderobjects.append(order_object)
            productId.append(cart_object.product_id)

        productobjects = []
        for j in productId:
            productobjects.append(
                Product.objects.get(id=j)
            )  # filtered queryset list where product id = filtered product ids
        info_dict_incomplete[order_object.id] = zip(cartobjects, productobjects)
        # For returning 0 items if there are no incomplete orders
    if Order.objects.filter(user=request.user, complete=False).exists():
        order = Order.objects.get(user=request.user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]

    context = {
        "userdetails": userdetails,
        "info_obj_incomplete": info_dict_incomplete,
        "cartItems": cartItems,
    }
    return render(request, "buyer/Order/Order History/incomplete_order.html", context)


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
    global form
    if SellerInfo.objects.filter(user=request.user, membership=True).exists():
        return HttpResponseRedirect("/seller/dashboard")
    else:
        if request.method == "POST":
            filled_form = SellerInfoForm(request.POST, request.FILES)
            if filled_form.is_valid():
                seller = SellerInfo()
                seller.user = request.user
                seller.businessname = filled_form.cleaned_data["businessname"]
                seller.business_phone_number = filled_form.cleaned_data[
                    "business_phone_number"
                ]
                seller.address = filled_form.cleaned_data["address"]
                seller.description = filled_form.cleaned_data["description"]
                seller.membership = True
                seller.image = filled_form.cleaned_data["image"]

                print("aklsfjklsadjf", type(seller.image), "when no input is given")
                seller.save()
                return HttpResponseRedirect("/seller/dashboard")

            else:
                for msg in filled_form.errors:
                    print(filled_form.errors[msg])
                return render(
                    request, "seller/seller_form.html", {"sellerform": filled_form}
                )
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
            unit_price = float(dish.price) * 100
            dish.product = filled_form.cleaned_data["product"]
            dish.seller = SellerInfo.objects.get(user=request.user)
            dish.image = filled_form.cleaned_data["image"]
            dish.servings = filled_form.cleaned_data["servings"]
            dish.category = filled_form.cleaned_data["category"]
            product = stripe.Product.create(name=dish.product, images=[dish.image])
            dish.stripe_product_id = product.id
            stripe_price = stripe.Price.create(
                unit_amount=int(unit_price),
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


# ability to edit food item on seller page/edit menu
@csrf_exempt
def edit_item(request):
    user_details = SellerInfo.objects.get(user=request.user)
    if request.method == "GET":
        return item(request)

    else:
        filled_form = DishInfoForm(request.POST, request.FILES)
        if filled_form.is_valid():
            dish = Product()

            # TODO : add price from Price Table
            dish.user = request.user
            dish.price = filled_form.cleaned_data["price"]
            unit_price = float(dish.price) * 100
            dish.product = filled_form.cleaned_data["product"]
            dish.seller = SellerInfo.objects.get(user=request.user)
            dish.image = filled_form.cleaned_data["image"]
            dish.servings = filled_form.cleaned_data["servings"]
            dish.category = filled_form.cleaned_data["category"]
            product = stripe.Product.create(name=dish.product, images=[dish.image])
            dish.stripe_product_id = product.id
            stripe_price = stripe.Price.create(
                unit_amount=int(unit_price),
                currency="cad",
                product=product.id,
            )
            dish.stripe_price_id = stripe_price.id
            dish.save()

            return HttpResponseRedirect("/seller/editmenu")
        else:

            for msg in filled_form.errors:
                print(filled_form.errors[msg])


# settings for buyer page
def buyer_settings(request):
    userdetails = BuyerInfo.objects.get(user=request.user)

    if request.method != "POST":
        user_details = BuyerInfo.objects.get(user=request.user)
        firstname = user_details.firstname
        lastname = user_details.lastname
        initial = {"firstname": firstname, "lastname": lastname}
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
    return render(request, "buyer/Restaurant/restaurants.html", context)


# adding item to cart
@csrf_exempt
def add_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    # https://stackoverflow.com/questions/61543829/django-taking-values-from-post-request-javascript-fetch-api

    item = post_data["product"]
    quantity = post_data["quantity"]
    product = Product.objects.get(product=item)
    currentCart = Cart.objects.filter(user=request.user).first()
    if currentCart is None or product.seller == currentCart.product.seller:
        orderdetails, created = Order.objects.get_or_create(
            user=request.user,
            buyer=BuyerInfo.objects.get(user=request.user),
            complete=False,
        )
        orderItem, created = Cart.objects.get_or_create(
            user=request.user,
            order=orderdetails,
            product=product,
            buyer=BuyerInfo.objects.get(user=request.user),
            quantity=quantity,
        )
        orderItem.save()

        return JsonResponse({'status': 'success'})
    else:

        return JsonResponse({'status': 'error'})


# deleting item from card
@csrf_exempt
def delete_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    # https://stackoverflow.com/questions/61543829/django-taking-values-from-post-request-javascript-fetch-api

    product_name = post_data["product"]
    user_id = request.user

    Cart.objects.get(
        product=Product.objects.get(product=product_name), user=user_id
    ).delete()

    return JsonResponse({"code": 200})


# update item from cart
@csrf_exempt
def modify_cart(request):
    post_data = json.loads(request.body.decode("utf-8"))
    item_id = post_data["product"]
    user_id = request.user.id
    quantity = post_data["quantity"]

    c = Cart.objects.get(user_id=user_id, id=item_id)
    c.quantity = quantity
    c.save()
    if request.user.is_authenticated:
        customer = request.user
        order, _ = Order.objects.get_or_create(
            user=customer,
            buyer=BuyerInfo.objects.get(user=request.user),
            complete=False,
        )
        cartTotal = order.get_cart_total
        cartItems = order.get_cart_items
    else:
        cartItems = 0
        cartTotal = 0

    return JsonResponse({"code": 200, "cartTotal": cartTotal, "cartItems": cartItems})


# cart page
def cart(request):
    userdetails = BuyerInfo.objects.get(user=request.user)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            user=customer,
            buyer=BuyerInfo.objects.get(user=request.user),
            complete=False,
        )
        items = order.cart_set.all()
        cartItems = order.get_cart_items

    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]

    context = {
        "items": items,
        "order": order,
        "userdetails": userdetails,
        "cartItems": cartItems,
    }
    return render(request, "buyer/Order/cart.html", context)


def delete_cart_item(request, id):
    try:
        Cart.objects.filter(user_id=request.user, id=id).delete()
    except:
        return HttpResponseRedirect("/cart")
    return HttpResponseRedirect("/cart")


@csrf_exempt
def menu(request):
    post_data = json.loads(request.body.decode("utf-8"))
    businessname = post_data["businessname"]
    request.session["businessname"] = businessname  # set 'businessname' in the session
    return JsonResponse({"code": 200})


def menu_page(request):
    token = request.session["businessname"]  # get 'token' from the session
    # renew session : request.session.pop('token', None)
    seller_details = SellerInfo.objects.get(businessname=token)
    food_details = Product.objects.filter(seller=seller_details)
    if Order.objects.filter(user=request.user, complete=False).exists():
        order = Order.objects.get(user=request.user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]
    context = {
        "item": token,
        "seller": seller_details,
        "food": food_details,
        "cartItems": cartItems,
    }
    return render(request, "buyer/Restaurant/menu.html", context)


def restaurants(request):
    if Order.objects.filter(user=request.user, complete=False).exists():
        order = Order.objects.get(user=request.user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]
    if request.method != "POST":
        form = searching_restaurants()
        FinalList = SellerInfo.objects.all()
        return render(
            request,
            "buyer/Restaurant/restaurants.html",
            {"form": form, "Restaurants": FinalList, "cartItems": cartItems},
        )
    elif request.method == "POST":
        filledform = searching_restaurants(request.POST)
        if filledform.is_valid():
            if filledform["name"].value() == "" and filledform["loc"].value() == "":
                prelistbyres = SellerInfo.objects.all()
            else:
                prelistbyres = SellerInfo.objects.filter(
                    businessname__icontains=filledform["name"].value(),
                    address__icontains=filledform["loc"].value(),
                )
            if filledform["name"].value() != "":
                prelistbydish = Product.objects.filter(
                    product__icontains=filledform["name"].value()
                )

            listbydish = []
            if filledform["name"].value() != "":
                for i in prelistbydish:
                    if filledform["loc"].value() in i.seller.address:
                        listbydish.append(i.seller)
            listbyres = []
            for i in prelistbyres:
                listbyres.append(i)
            FinalList = listbyres + listbydish
            FinalList = list(dict.fromkeys(FinalList))

            return render(
                request,
                "buyer/Restaurant/restaurants.html",
                {"form": filledform, "Restaurants": FinalList, "cartItems": cartItems},
            )
        else:
            for msg in filledform.errors:
                print(filledform.errors[msg])
                form = searching_restaurants()
                FinalList = SellerInfo.objects.all()
                return render(
                    request,
                    "buyer/Restaurant/restaurants.html",
                    {"form": form, "Restaurants": FinalList, "cartItems": cartItems},
                )
