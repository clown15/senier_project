from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import FormView
from .forms import SignUpForm,SignInForm,AllergyForm,AllergyLevelForm
from django.contrib.auth.hashers import make_password
from .models import User,Allergy,DegreeOfAllergy
from django.forms.models import model_to_dict
from utils.product_related import *
from utils.als import *
from product.models import *
from order.models import *
from django.db.models import Count,F,Subquery

# Create your views here.

def index(request):
    # 구매내역 기반 상품 추천
    if request.session.get('user'):
        login_user = request.session.get('user')
        min_orders = 2  # 사용자 주문 횟수
        min_order_user = 2  # 사용자 주문 횟수가 min_orders이상인 사용자 수
        # 사용자 주문 횟수
        user_history = Order.objects.filter(orderer=login_user).count()
        # 특정 횟수 이상 주문한 사용자들(로그인한 사용자 제외)
        orders = Order.objects.values('orderer').annotate(
            max_count=Count('product'),
            user=F('orderer')
        ).filter(max_count__gte=min_orders).exclude(user=login_user).values('max_count', 'user')

        if user_history >= min_orders and orders.count() >= min_order_user:
            product_list = als_product_recommendation(request.session)
        else:
            product_list = product_recommendation_for_metadata(request.session)
    else:
        product_list = Product.objects.order_by('-sales_rate')[:5]

    # 최신 상품 추천
    new_products = Product.objects.order_by('-creation_date')[:5]
    
    # 가장 최근 팔린 상품 추천
    hot_products = hot_product_recommendation()

    # 상품 이미지 등록
    for product in product_list:
        try:
            product.image = product.images.filter(product = product)[0].image
        except:
            product.image = "images/noimage.gif"
    
    for product in new_products:
        try:
            product.image = product.images.filter(product = product)[0].image
        except:
            product.image = "images/noimage.gif"

    for product in hot_products:
        try:
            product.image = product.images.filter(product = product)[0].image
        except:
            product.image = "images/noimage.gif"


    return render(request, 'index.html',{'email':request.session.get('user'), 'product_list':product_list, 'new_products':new_products, 'hot_products':hot_products})

# 상품 메타데이터와 알러지 정보 동기화
# def test():
#     product_meta_data = MetaData.objects.all()

#     for meta_data in product_meta_data:
#         allergy = meta_data.product.allergy.all()
#         if len(allergy) > 0:
#             if meta_data.product == allergy[0].product:
#                 meta_data.allergy = allergy[0]
                
#                 meta_data.save()

def SignOut(request):
    if "user" in request.session:
        del(request.session['user'])

    return redirect('/')


class SignUpView(FormView):
    template_name = "signup.html"
    # form_class = AllergyForm
    form_class = AllergyLevelForm
    success_url = "/signin/"


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     for v in context['form']:
    #         print(v.__dict__)

    #     return context

    def form_valid(self,form):
        user = User(
            email = form.data.get('email'),
            password = make_password(form.data.get('password')),
            level = form.data.get('level'),
        )

        user.save()

        allergy_level = DegreeOfAllergy(
            user = user,
            buckwheat = form.data.get('buckwheat'),
            wheat = form.data.get('wheat'),
            Big_head = form.data.get('Big_head'),
            peanut = form.data.get('peanut'),
            Walnut = form.data.get('Walnut'),
            pine_nut = form.data.get('pine_nut'),
            peach = form.data.get('peach'),
            tomato = form.data.get('tomato'),
            milk = form.data.get('milk'),
            shrimp = form.data.get('shrimp'),
            Mackerel = form.data.get('Mackerel'),
            squid = form.data.get('squid'),
            crab = form.data.get('crab'),
            clam = form.data.get('clam'),
            Pork = form.data.get('Pork'),
            beef = form.data.get('beef'),
            chicken = form.data.get('chicken'),
        )

        allergy_level.save()


        return super().form_valid(form)


class SignInView(FormView):
    template_name = 'signin.html'
    form_class = SignInForm
    success_url = "/"

    # form유효성 검사끝난후 실행
    def form_valid(self,form):        
        user = get_object_or_404(User, email=form.data.get('email'))

        self.request.session['user'] = form.data.get('email')
        self.request.session['level'] = user.level
        
        # 사용자 알러지정보에서 사용자, 알러지 테이블ID 삭제하고 세션에 저장
        # {'id': 2, 'user': 'user2@test.com', 'buckwheat': 0, 'wheat': 0, 'Big_head': 0, 'peanut': 2, 'Walnut': 1, 'pine_nut': 0, 'peach': 0, 'tomato': 0, 'milk': 0, 'shrimp': 0, 'Mackerel': 0, 'squid': 0, 'crab': 0, 'clam': 0, 'Pork': 0, 'beef': 0, 'chicken': 0}
        user_allergy = model_to_dict(DegreeOfAllergy.objects.defer('id','user').get(user=user))

        del user_allergy['id']
        del user_allergy['user']
        self.request.session['user_allergy'] = user_allergy

        return super().form_valid(form)