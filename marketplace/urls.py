"""
URL configuration for foodApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
    path('', views.marketplace, name='marketplace'),
    # CART
    path('cart/', views.cart, name='cart'),

    path('<slug:vendor_slug>', views.vendor_detail, name='vendor_detail'),

    # ADD_TO_CART
    path('add_to_cart/<int:food_id>', views.add_to_cart, name='add_to_cart'),
    # decrease_cart
    path('decrease_cart/<int:food_id>', views.decrease_cart, name='decrease_cart'),
    
    #delete cart
    path('delete_cart/<int:cart_id>', views.delete_cart, name='delete_cart'),

    
] 
