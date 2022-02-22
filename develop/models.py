from django.contrib.auth.models import User
from django.db import models


#  this is where we will add the tables for our database

# commands to remember :
# python manage.py migrate
# python  manage.py makemigrations

# Create your models here.
# TODO: Buyer Table : Kweku and Vineeth
# Please NOTE : make sure to add migrations


# TODO: Seller Table : Vijay and Shubham
# Please NOTE : make sure to add migrations






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
