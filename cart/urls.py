"""EcomShoppers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('usercart', views.usercart, name='usercart'),
    path('add_cart', views.add_cart, name='add_cart'),
    path('deletecart_item<cart_id>/', views.deletecart_item, name='deletecart_item'),
    path('updatecart', views.updatecart, name='updatecart'),
    path('orderdetails/<int:id>/', views.orderdetails, name='orderdetails'),
    path('ordercancel/<int:id>/',views.ordercancel,name='ordercancel') ,
    path('wishlist', views.wishlist, name="wishlist"),
    path('add_wishlist/<int:cart_id>/', views.add_wishlist, name="add_wishlist"),
    path('wishlist/<slug>/', views.add_direct_wishlist , name='add_direct_wishlist'),
    ]
    
