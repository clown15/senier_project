from django.shortcuts import render
from django.views.generic import ListView
from user.models import User
from django.utils.decorators import method_decorator
from user.decorators import login_required
from .models import Cart
from product.models import Product
from user.models import User

from django.db import transaction
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

@method_decorator(login_required, name="dispatch")
class CartList(ListView):
    template_name = "cart_list.html"
    context_object_name = "cart_list"

    def get_queryset(self, **kwargs):
        queryset = Cart.objects.filter(user = self.request.session.get('user')).order_by('-creation_date')

        return queryset

class CartAPI(APIView):
    def post(self,request):
        product = Product.objects.get(pk=request.data['product'])
        quantity = int(request.data['quantity'])

        with transaction.atomic():
            cart = Cart(
                total_price = product.price * quantity,
                quantity = quantity,
                product = product,
                seller = product.creator,
                user = User.objects.get(email=self.request.session.get('user')),
            )

            cart.save()

        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        with transaction.atomic():
            cart = Cart.objects.get(pk=request.data['pk'])
            
            if self.request.session.get('user') == cart.user.email:
                cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
