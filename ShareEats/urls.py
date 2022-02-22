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
from django.urls import path, include, re_path
from develop import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # buyer or seller option page
    path('buyer_seller_option', views.buyer_seller_option, name='option'),
    path('buyer_dashboard', views.buyer_dashboard, name='buyer dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    # login for authentication
    path('', auth_views.LoginView.as_view(), name='login'),
    # logout for authentication
    path('logout', views.logout_view, name='logout'),
    # signing up for authentication
    path('sign_up', views.sign_up, name="sign up"),
    path('selleradditonalinformation', views.seller_form, name='seller info'),
    path('buyeradditonalinformation', views.buyer_form, name='buyer info'),
    # path('buyersign_up', views.buyer_signup, name="sign up"),
    # path('buyersign_in', views.buyer_signin, name='buyersign in'),

    # Added test comment
]
