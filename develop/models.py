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


class Product(models.Model):
    product = models.CharField(max_length=30)
    stripe_product_id = models.CharField(max_length=100)
    quantity = models.IntegerField()
    stripe_price_id = models.CharField(max_length=100)
    price = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    # file will be uploaded to MEDIA_ROOT / uploads
    image = models.ImageField(upload_to='images')
    seller = models.ForeignKey(SellerInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    payment_id = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerInfo, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    buyer = models.ForeignKey(BuyerInfo, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_total(self):
        total = int(self.product.price) * self.quantity
        return total
