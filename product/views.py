from django.shortcuts import render,get_object_or_404
import re
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView,UpdateView
from .models import Product,Images,Allergy,MetaData
from .forms import Product_Register
from order.forms import RegisterForm as OrderForm
from django.utils.decorators import method_decorator
from user.decorators import admin_required
from user.models import User
from user.models import Allergy as User_Allergy
from django.contrib.messages import get_messages
from ast import literal_eval
from utils.vision_api import detect_text, check_word_in_list, model_to_dict_allergy
from utils.product_related import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,generics,mixins
from django.db import transaction
from django.forms.models import model_to_dict
from django.db import connection

# Create your views here.

def product_index(request):
    return render(request, 'product_list_temp.html')
# 상품 전체 리스트
class productList(ListView):
    model = Product
    template_name = "product.html"
    context_object_name = "product_list"
    # ordering = ['-creation_date'] # 정렬
    # paginate_by = 5 # 한 페이지에 보여줄 데이터 수

    def get_queryset(self):
        if 'category' in self.kwargs:
            return Product.objects.filter(category = self.kwargs['category']).order_by('-creation_date')
        else:
            #return Product.objects.all().order_by('-creation_date')[:5] # 한페이지에 5개 데이터 표시
            return Product.objects.all().order_by('-creation_date')

    def get_context_data(self,**kwargs):
        # 기본 구현을 호출해 context를 가져온다
        # context = super(ProductDetail, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        for product in context['product_list']:
            total_count = 0
            count = 0
            
            if self.request.session.get('user'):
                if product.allergy.all():
                    product_allergy_dict = model_to_dict(product.allergy.all()[0])
                    for k,v in self.request.session['user_allergy'].items():
                        if v:
                            total_count +=1
                            if product_allergy_dict[k]:
                                count += 1
                # if total_count != 0:
                #     product.fit = (1-count/total_count)*100
                # else:
                #     product.fit = 100
                product.fit = count

            img = Images.objects.filter(product = product)
            if img:
                product.image = img[0].image

        return context

# 등록한 상품을 보여주는 리스트
class productListAdmin(ListView):
    # model = Product
    template_name = "product_list.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.filter(creator=self.request.session.get('user')).order_by('-creation_date')

@method_decorator(admin_required,name="dispatch")
class ProductRegister(FormView):
    template_name = 'product_register.html'
    form_class = Product_Register
    success_url = '/product/manage/'

    # forms.py에 있는 Product_Register로 form의 값이 넘어 가기 전에 실행되는 함수로 forms.py 에서 request.session를 사용하기 위함.(이걸 사용하지 않으면 forms.py에서 request를 사용할 수 없음)
    # def get_form_kwargs(self,**kwargs):
    #     kw = super().get_form_kwargs(**kwargs)
    #     kw.update({
    #         "request":self.request,
    #     })
    #     return kw
    
    def form_valid(self,form):
        # 상품 등록
        if "Nutrition_Facts" in self.request.FILES:
            Nutrition_Facts = self.request.FILES['Nutrition_Facts']
        else:
            Nutrition_Facts = None

        product = Product(
            name = form.data.get('name'),
            price = form.data.get('price'),
            category = form.data.get('category'),
            info = form.data.get('info'),
            Nutrition_Facts = Nutrition_Facts,
            creator = User.objects.get(email=self.request.session.get('user'))
        )      
        product.save()
        
        
        if Nutrition_Facts != None:
            # 상품 정보에서 알러지 정보 추출 및 저장
            # img_path = "/home/Administrator/django_shop/Django_Shop/media" + product.Nutrition_Facts.url
            # response = detect_text(img_path)
            # texts = response.text_annotations
            
            # text_list = []
            # for text in texts:
            #     content = text.description
            #     content = content.replace(',','')
            #     text_list.append(content)
            
            # allergy_info = check_word_in_list(text_list)

            # allergy = Allergy (
            #     product = product,
            #     buckwheat = allergy_info['buckwheat'],
            #     wheat = allergy_info['wheat'],
            #     Big_head = allergy_info['Big_head'],
            #     peanut = allergy_info['peanut'],
            #     Walnut = allergy_info['Walnut'],
            #     pine_nut = allergy_info['pine_nut'],
            #     peach = allergy_info['peach'],
            #     tomato = allergy_info['tomato'],
            #     milk = allergy_info['milk'],
            #     shrimp = allergy_info['shrimp'],
            #     Mackerel = allergy_info['Mackerel'],
            #     squid = allergy_info['squid'],
            #     crab = allergy_info['crab'],
            #     clam = allergy_info['clam'],
            #     Pork = allergy_info['Pork'],
            #     beef = allergy_info['beef'],
            #     chicken = allergy_info['chicken'],
            # )
            allergy_information_extraction(product)
        
        # 상품 사진 저장
        for img in self.request.FILES.getlist('images'):
            image = Images(
                product = product,
                image = img
            )

            image.save()


        return super().form_valid(form)

class ProductDetail(DetailView):
    template_name = 'detail.html'
    queryset = Product.objects.all()
    # html에서 사용할 변수명
    context_object_name = "product"

    # 생성된 forms.py를 기반으로 생성된 form에 원하는 form을 추가하기위함
    def get_context_data(self,**kwargs):
        # 기본 구현을 호출해 context를 가져온다
        # context = super(ProductDetail, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request)
        
        context['images'] = Images.objects.filter(product = context['product'])
        try:
            context['allergys'] = model_to_dict_allergy(Allergy.objects.get(product = context['product']))
        except:
            context['allergys'] = {}

        return context

    def form_valid(self,form):
        product = Product(
            name = form.data.get('name'),
            price = form.data.get('price'),
            stock = form.data.get('stock'),
            info = form.data.get('info'),
            creator = User.objects.get(email=self.request.session.get('user')),
        )
        product.save()

        return super().form_valid(form)

class ProductUpdate(FormView):
    model = Product
    template_name = 'product_update.html'
    form_class = Product_Register
    success_url = '/product/manage/'

    # def get_object(self):
    #     product = get_object_or_404(Product, pk=self.kwargs['pk'])

    #     return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = model_to_dict(get_object_or_404(Product, pk=self.kwargs['pk']))

        return context
    
    def form_valid(self,form):

        if "Nutrition_Facts" in self.request.FILES:
            Nutrition_Facts = self.request.FILES['Nutrition_Facts']
        else:
            Nutrition_Facts = None

        product = Product.objects.get(pk=self.kwargs['pk'])


        name = form.data.get('name').strip()
        price = form.data.get('price').strip()
        category = form.data.get('category')
        info = form.data.get('info').strip()

        product.name  = name
        product.price = price
        product.category = category
        product.info  = info
        
        product.save(force_update = True,update_fields=['name', 'price', 'category', 'info'])

        if Nutrition_Facts != None:
            allergy_information_extraction(product)

        # 상품 사진이 있을경우 저장
        if self.request.FILES.getlist('images') != None:
            for img in self.request.FILES.getlist('images'):
                image = Images(
                    product = product,
                    image = img
                )

                image.save()

        return super().form_valid(form)

class ProductDeleteAPI(APIView):
    def delete(self, request, pk, format=None):
        with transaction.atomic():
            product = Product.objects.get(pk=pk)

            user = request.data.get('user')
            if user == product.creator.email:
                product.delete()
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
        return Response(status=status.HTTP_204_NO_CONTENT)



# 상품 정보에서 알러지 정보 추출 및 저장
def allergy_information_extraction(product):
    img_path = "/home/Administrator/django_shop/Django_Shop/media" + product.Nutrition_Facts.url
    response = detect_text(img_path)
    texts = response.text_annotations
    
    text_list = []
    for text in texts:
        content = []
        for word in re.split('[,.\n]',text.description):
            if len(word) > 0:
                content.append(word)
        text_list.extend(content)

    
    allergy_info = check_word_in_list(text_list)

    allergy = Allergy (
        product = product,
        buckwheat = allergy_info['buckwheat'],
        wheat = allergy_info['wheat'],
        Big_head = allergy_info['Big_head'],
        peanut = allergy_info['peanut'],
        Walnut = allergy_info['Walnut'],
        pine_nut = allergy_info['pine_nut'],
        peach = allergy_info['peach'],
        tomato = allergy_info['tomato'],
        milk = allergy_info['milk'],
        shrimp = allergy_info['shrimp'],
        Mackerel = allergy_info['Mackerel'],
        squid = allergy_info['squid'],
        crab = allergy_info['crab'],
        clam = allergy_info['clam'],
        Pork = allergy_info['Pork'],
        beef = allergy_info['beef'],
        chicken = allergy_info['chicken'],
    )

    allergy.save()
    metadata = create_product_meta(product,text_list, allergy)

    return allergy


def create_product_meta(product, text_list, allergy):
    metadata = MetaData(
        product = product,
        data = " ".join(text_list),
        allergy = allergy,
    )

    metadata.save()