# dj_razorpay/urls.py

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('paymenttest', views.homepage, name='index'),
	
]
