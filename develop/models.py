from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

#  this is where we will add the tables for our database
"""

"""


# commands to remember :
# python manage.py migrate
# python  manage.py makemigrations
class User(AbstractUser):
    phone = models.TextField(max_length=20, blank=False)
    is_verified = models.BooleanField(default=False)


class SellerInfo(models.Model):
    businessname = models.CharField(max_length=20)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16)
    address = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.BooleanField(default=False)


class BuyerInfo(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.BooleanField(default=False)


class DishInfo(models.Model):
    product = models.CharField(max_length=30)
    stripe_product_id = models.CharField(max_length=100)
    quantity = models.IntegerField()
    category = models.CharField(max_length=20)
    # file will be uploaded to MEDIA_ROOT / uploads
    image = models.ImageField(upload_to='images')
    seller = models.ForeignKey(SellerInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Price(models.Model):
    product = models.ForeignKey(DishInfo, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    seller = models.ForeignKey(SellerInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class CartItem(models.Model):
    product = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerInfo, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Order(models.Model):
    payment_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerInfo, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    product = models.CharField(max_length=20)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Price, on_delete=models.CASCADE)
