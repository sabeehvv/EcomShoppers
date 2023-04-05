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
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from products.consumer import AdminNotificationConsumer
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
# from products.consumer import OrderConsumer

# application = ProtocolTypeRouter({
#     'websocket': URLRouter([
#         path('ws/admin_notifications/', AdminNotificationConsumer.as_asgi()),
#     ]),
# })  


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"^ws/admin_notifications/$", AdminNotificationConsumer.as_asgi()),
        ])
    ),
})


urlpatterns = [
    path('adminpage/', admin.site.urls),
    path('product/', include('products.urls')),
    path('', include('homeuser.urls')),
    path('', include('login.urls')),
    path('admin/', include('adminpage.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        
urlpatterns += staticfiles_urlpatterns()



