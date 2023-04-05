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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('qqww', views.home1),
    path('cart', views.cart),
    path('userheader', views.userheader),
    path('', views.userhome ,name='userhome'),
    path('usershop', views.usershop, name='usershop'),
    path('filter-products/', views.filter_products, name='filter-products'),
    path('Category<slug>/', views.get_category , name='get_category'),
    path('filter_products', views.filter_products, name='filter_products'),
    path('test/', views.test, name="home"),
]
