from django.contrib import admin
from . models import *

# Register your models here.





@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['quantity' , 'cartprice' , 'sizevariant']
    model = CartItem


@admin.register(Address)
class userAddress(admin.ModelAdmin):
    list_display = ['firstname' , 'city' , 'pincode']
    model = Address


admin.site.register(Cart)
