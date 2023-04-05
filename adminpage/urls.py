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
    path('', views.adminpage ,name='adminpage'),  
    path('logins', views.adminlogins, name='adminlogins'), 
    path('aduser', views.aduser ,name='aduser'),  
    path('logoutadmin', views.logoutadmin , name='logoutadmin'),
    path('search_username', views.search_username,name='search_username'),
    path('update_user', views.update_user,name='update_user'),
    path('admincategory', views.admincategory,name='admincategory'),
    path('admincategoryedit', views.admincategoryedit,name='admincategoryedit'),
    path('adminproduct', views.adminproduct,name='adminproduct'),
    path('addcategory', views.addcategory,name='addcategory'),
    path('editcategory', views.editcategory,name='editcategory'),
    path('addproduct', views.addproduct,name='addproduct'),
    path('deleteproduct', views.deleteproduct,name='deleteproduct'),
    path('<slug>/', views.editproduct,name='editproduct'),
    path('deletecategory', views.deletecategory,name='deletecategory'),
    path('adminorder', views.adminorder,name='adminorder'),
    path('orderdetailsadmin/<int:id>/',views.orderdetailsadmin,name='orderdetailsadmin') ,
    path('orderstatus/<int:id>/',views.orderstatus,name='orderstatus')  ,
    path('deletorder_item/<int:order_id>/',views.deletorder_item,name='deletorder_item')  ,
    path('order_filter', views.order_filter,name='order_filter'),
]
