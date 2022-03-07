from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

#  this is where we will add the tables for our database
"""

"""


# commands to remember :
# python manage.py migrate
# python  manage.py makemigrations


class SellerInfo(models.Model):
    businessname = models.CharField(max_length=20)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16)
    address = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    cardnumber = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)
    expiry_date = models.CharField(max_length=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.BooleanField(default=False)


class BuyerInfo(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.BooleanField(default=False)


# git using pycharm
class DishInfo(models.Model):
    item = models.CharField(max_length=30)
    price = models.CharField(max_length=5)
    quantity = models.IntegerField()
    category = models.CharField(max_length=20)
    # file will be uploaded to MEDIA_ROOT / uploads
    image = models.ImageField(upload_to='images')
    seller_id = models.ForeignKey(SellerInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
