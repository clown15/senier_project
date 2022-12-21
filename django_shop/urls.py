"""django_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from user.views import index,SignOut,SignUpView,SignInView
from product.views import *
from order.views import (
    OrderCreate,OrderList,OrderCancel,OrderAPI
)
from cart.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('signup/',SignUpView.as_view()),
    path('signin/',SignInView.as_view()),
    path('signout/',SignOut),
    path('product/',productList.as_view()),
    path('product/<int:pk>/',ProductDetail.as_view(), name="detail"),
    path('product/create/',ProductRegister.as_view()),
    path('product/manage/',productListAdmin.as_view()),
    path('product/<str:category>/',productList.as_view()),
    path('product/update/<int:pk>/', ProductUpdate.as_view()),
    path('api/product/<int:pk>', ProductDeleteAPI.as_view()),
    path('order/create/',OrderCreate.as_view()),
    path('order/',OrderList.as_view()),
    path('order/cancel/',OrderCancel.as_view()),
    # path('api/order/create/',OrderCreateAPI.as_view()),
    path('api/order/',OrderAPI.as_view(), name="order_api"),
    path('cart/',CartList.as_view(), name="cart_list"),
    path('api/cart/',CartAPI.as_view(), name="cart_api"),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
