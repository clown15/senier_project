from django import forms
from .models import Product
from user.models import User

class Product_Register(forms.ModelForm):
    # def __init__(self,request,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.request = request

    class Meta:
        model = Product
        fields = ['name',]

    # name = forms.CharField(
    #     error_messages = {
    #         'required':'상품명을 입력하세요.'
    #     },max_length=256,
    #     label = "상품명"
    # )
    price = forms.IntegerField(
        error_messages = {
            'required':'가격을 입력하세요.'
        },
        label = "가격"
    )
    category = forms.ChoiceField(
        error_messages = {
            'required':'종류를 선택하세요.'
        },
        choices =(
            ("vegetable","채소"),
            ("fruit","과일"),
            ("nut","견과"),
            ("rice","쌀"),
            ("fisheries, seafood","수산,해산"),
            ("meat, eggs","정육,계란"),
            ("Soup, side dish, main dish","국,반찬,메인요리"),
            ("salad","샐러드"),
            ("noodle","면"),
            ("beverage","음료"),
            ("Snack","간식"),
            ("etc","기타"),
        ),
        # 초기값 설정
        initial = "etc",
        label = "종류",
    )
    images = forms.ImageField(
        label = "상품 사진",
        required = False,
    )
    info = forms.CharField(
        widget=forms.Textarea,
        label = "상품설명",
        required = False,
    )
    Nutrition_Facts = forms.ImageField(
        label = "영양정보",
        required = False,
    )
    

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')
        info = cleaned_data.get('info')


        if not name:
            self.add_error('name','상품명을 입력하세요.')
        if not price:
            self.add_error('price','상품가격을 입력하세요.')
        if not info:
            self.add_error('info','상품 정보를 입력하세요.')
        # if not stock:
        #     self.add_error('stock','수량을 입력하세요.')
            