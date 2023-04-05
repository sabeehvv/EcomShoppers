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
from .consumer import AdminNotificationConsumer


urlpatterns = [
    path('single/<slug>/', views.get_product , name='get_products'),
    path('checkout', views.checkout, name='checkout'),
    path('useraccount', views.useraccount, name='useraccount'),
    path('addaddress', views.addaddress, name='addaddress'),
    path('deleteaddress/<int:id>/',views.deleteaddress,name='deleteaddress') ,
    path('ordersend', views.ordersend, name='ordersend'),
    path('payment_confirm', views.payment_confirm, name='payment_confirm'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path("order_return/<int:id>/", views.order_return, name="order_return"),
    path('wishlist_to_cart/<int:cart_id>/', views.wishlist_to_cart, name="wishlist_to_cart"),
    ]
    

