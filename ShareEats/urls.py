"""ShareEats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()

"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
# import settings and static first
from django.conf import settings
from django.conf.urls.static import static
from develop import views
from develop.views import CancelView

urlpatterns = [
    path('admin/', admin.site.urls),
    # buyer or seller option page
    path('option', views.buyer_seller_option, name='option'),
    path('buyer/dashboard', views.buyer_dashboard, name='buyer dashboard'),
    path('seller/dashboard', views.seller_dashboard, name='seller dashboard'),
    path('seller/editmenu', views.editmenu, name='edit menu'),
    path('seller/settings', views.seller_settings, name='seller settings'),
    path('seller/additem', views.add_item, name='add product'),
    path('seller/edititem', views.edit_item, name='edit product'),
    path('seller/item', views.item, name='item editing'),
    path('seller/deleteitem', views.delete_food_item, name='delete food'),
    path('buyer/settings', views.buyer_settings, name='buyer settings'),
    path('buyer/orders', views.order, name='order'),
    path('buyer/adddishitem', views.add_item, name='adddish product'),
    path('buyer/favourites', views.favourites, name='favourites'),
    path('accounts/', include('django.contrib.auth.urls')),
    # login for authentication
    path('', auth_views.LoginView.as_view(), name='login'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/Password/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/Password/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/Password/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/Password/password_reset_done.html"),
         name="password_reset_complete"),
    # logout for authentication
    path('logout', views.logout_view, name='logout'),
    # signing up for authentication
    path('sign_up', views.sign_up, name="sign up"),
    path('seller/selleradditonalinformation', views.seller_form, name='seller info'),
    path('buyer/buyeradditonalinformation', views.buyer_form, name='buyer info'),
    path('seller/report', views.reports, name='report'),
    path('buyer/restaurants', views.restaurants, name='buyer restaurants'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', views.Success, name='success'),
    path('create-checkout-session/', views.CreateCheckoutSessionView, name='create-checkout-session'),
    path('loginverification', views.login_verify_code, name='verify_login'),
    # 2fa authentication
    path('verify/', views.verify_code, name='verify'),
    path('menu/', views.menu, name='menu'),
    path('buyer/menu/', views.menu_page, name='menupage'),
    path("add-cart/", views.add_cart),
    path("delete-cart/", views.delete_cart),
    path("modify-item/", views.modify_cart),
    path("cart/", views.cart, name='cart'),

]

# add this lines
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
