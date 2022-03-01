from django.contrib.auth.models import User
from django.db import models


#  this is where we will add the tables for our database

# commands to remember :
# python manage.py migrate
# python  manage.py makemigrations


class SellerInfo(models.Model):
    businessname = models.CharField(max_length=20)
    phone = models.IntegerField()
    address = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    cardnumber = models.IntegerField()
    Cvv = models.IntegerField()
    ExpiryDate = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.businessname


class BuyerInfo(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    phone = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname


class DishInfo(models.Model):
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
