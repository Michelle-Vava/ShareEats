from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


#  this is where we will add the tables for our database

# commands to remember :
# python manage.py migrate
# python  manage.py makemigrations

# Create your models here.
# TODO: Buyer Table : Kweku and Vineeth
# Please NOTE : make sure to add migrations


class buyersignup(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )  # validators should be a list
    user_name = models.CharField(max_length=100)


# TODO: Seller Table : Vijay and Shubham
# Please NOTE : make sure to add migrations
# Hi I was here : Michelle Vava


# need more information here
# class SellerInfo(models.Model):
#     firstname = models.CharField(max_length=20)
#     lastname = models.CharField(max_length=20)
#
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.firstname
#
#
# class DishInfo(models.Model):
#     price = models.IntegerField()
#     quantity = models.IntegerField()
#     category = models.CharField(max_length=20)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
