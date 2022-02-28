from django.contrib.auth.models import User
from django.db import models
#from phonenumber_field.models import PhoneNumber

#  this is where we will add the tables for our database

# commands to remember :
# python manage.py migrate
# python  manage.py makemigrations

# Create your models here.
# TODO: Buyer Table : Kweku and Vineeth
# Please NOTE : make sure to add migrations


# TODO: Seller Table : Vijay and Shubham
# Please NOTE : make sure to add migrations
#  Add Something


# need more information here
class SellerInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buisnessName = models.CharField(max_length=128)
    seller_email = models.EmailField()
    seller_address = models.CharField(max_length=128)
    seller_phone = models.IntegerField(max_length=10)
    company_desc = models.CharField(max_length=128)
    card_number = models.IntegerField(max_length=16)
    exp_month = models.IntegerField(max_length=2)
    exp_year = models.IntegerField(max_length=2)
    cvv = models.IntegerField(max_length=3)
    
#
    def __str__(self):
        return self.buisnessName
#
#
# class DishInfo(models.Model):
#     price = models.IntegerField()
#     quantity = models.IntegerField()
#     category = models.CharField(max_length=20)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
