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
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
# import settings and static first
from django.conf import settings
from django.conf.urls.static import static
from develop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # buyer or seller option page
    path('option', views.buyer_seller_option, name='option'),
    path('buyer/dashboard', views.buyer_dashboard, name='buyer dashboard'),
    path('seller/dashboard', views.seller_dashboard, name='seller dashboard'),
    path('seller/editmenu', views.editmenu, name='edit menu'),
    path('seller/settings', views.seller_settings, name='seller settings'),
    path('seller/additem', views.add_item, name='add item'),
    path('buyer/settings', views.buyer_settings, name='buyer settings'),
    path('buyer/orders', views.order, name='order'),
    path('buyer/favourites', views.favourites, name='favourites'),
    path('buyer/checkout', views.checkout, name='checkout'),
    path('accounts/', include('django.contrib.auth.urls')),
    # login for authentication
    path('', auth_views.LoginView.as_view(), name='login'),
    # logout for authentication
    path('logout', views.logout_view, name='logout'),
    # signing up for authentication
    path('sign_up', views.sign_up, name="sign up"),
    path('seller/selleradditonalinformation', views.seller_form, name='seller info'),
    path('buyer/buyeradditonalinformation', views.buyer_form, name='buyer info'),
    path('seller/report', views.reports, name='report'),
    path('buyer/restaurants', views.buyer_dashboard, name='buyer restaurants'),

]
# add this lines
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
