from django.db import models
from products.models import Product , SizeVariant
from login.models import CustomUser
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartitems")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    sizemodel = models.ForeignKey(SizeVariant, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    sizevariant = models.CharField(max_length=10, blank=True)
    cartprice = models.FloatField(null=True)
    is_active = models.BooleanField(default=True)
    buy_now = models.BooleanField(default=False)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class Address(models.Model):
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    phonenumber = models.CharField(max_length=50, null=True)
    housename = models.CharField(max_length=50, null=True)
    town = models.CharField(max_length=50, null=True)
    locality = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.last_name
