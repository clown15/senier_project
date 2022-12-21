from django.shortcuts import render,redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import RegisterForm,CancelForm
from user.models import User
from django.utils.decorators import method_decorator
from user.decorators import login_required
from .models import Order
from product.models import Product
from django.db import transaction
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,generics,mixins
from .serializers import OrderSerializer

# Create your views here.

@method_decorator(login_required,name="dispatch")
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/order/'

    # form을 생성할때 사용할 인자값을 정하는? 함수
    def get_form_kwargs(self,**kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            "request":self.request,
        })
        return kw

    # 값이 성공적으로 들어오면 실행되는 함수
    def form_valid(self,form):
        product = form.product
        quantity = int(form.data.get('quantity'))
        
        with transaction.atomic():
            order = Order(
                quantity = quantity,
                product = product,
                seller = product.creator,
                orderer = User.objects.get(email=self.request.session.get('user')),
                total_price = product.price * quantity,
            )

            order.save()

            product.sales_rate += quantity
            product.save()
            
        return super().form_valid(form)

    # 값이 제대로 안들어 왔을때
    def form_invalid(self,form):
        return render(self.request, 'detail.html', {'form': form, 'product':form.product})

# decorator호출
# class view로 접근시 dispatch함수 호출
# 원칙은 decorator사용시 method에 사용해야 하나 아래 방식처럼 하면 클래스에 사용가능
# from django.utils.decorators import method_decorator를 통해 사용가능
# @method_decorator(decorator_name,method_name)
# 어떤 method 에 어떤 decorator를 적용할지 작성
# 일반적으로 사용할시 
# @login_required
# def dispatch(request,*args,**kwargs)
# 이런식으로 사용가능
@method_decorator(login_required,name="dispatch")
class OrderList(ListView):
    template_name="order_list.html"
    context_object_name="order_list"

    def get_queryset(self,**kwargs):
        queryset=Order.objects.filter(orderer=self.request.session.get('user')).order_by('-creation_date')

        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CancelForm()
        
        return context

@method_decorator(login_required,name="dispatch")
class OrderCancel(FormView):
    form_class = CancelForm
    success_url = '/order'

    def form_valid(self,form):
        with transaction.atomic():    
            order = Order.objects.get(pk=form.data.get('cancel'))
            product = Product.objects.get(pk=order.product.id)            
            product.sales_rate -= order.quantity

            order.delete()
            product.save()

        return redirect('/order/')

    def form_invalid(self,form):
        return redirect('/order/')

# class OrderCreateAPI(generics.GenericAPIView,mixins.CreateModelMixin):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
    
#     def post(self,request,*args,**kwargs):
#         return self.create(self,*args,**kwargs)

# class OrderCreateAPI(APIView):
#     def post(self, request, format=None):
#         serializer = OrderSerializer(data=request.data)
#         print(self)
#         # if serializer.is_valid():
#         #     serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OrderDeleteAPI(generics.GenericAPIView,mixins.DestroyModelMixin):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def delete(self, request, *args, **kwargs):
#         with transaction.atomic():    
#             order = Order.objects.get(pk=kwargs.get('pk'))
#             product = Product.objects.get(pk=order.product.id)
            
#             order.delete()
#             product.stock += order.quantity
#             product.save()
            
#         return self.destroy(request, *args, **kwargs)
class OrderAPI(APIView):
    def put(self, request):
        order = Order.objects.get(id=request.data['id'])
        order.rate = request.data['rate']
        order.save()

        return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk, format=None):
        with transaction.atomic():    
            order = Order.objects.get(pk=pk)
            if self.request.session.get('user') == order.orderer:
                product = Product.objects.get(pk=order.product.id)
                product.sales_rate -= order.quantity

                order.delete()
                product.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
