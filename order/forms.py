from django import forms
from django.contrib import messages
from product.models import Product

class RegisterForm(forms.Form):
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages = {
            'required':'수량을 입력하세요.'
        },label = '수량'
    )
    product = forms.IntegerField(
        label = '상품',
        widget = forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        
        # views.py 에서 product값을 사용해 redirect하기위함
        self.product = Product.objects.get(pk=product)
        if quantity and quantity <= 0:
            self.add_error('quantity',"입력된 값이 정상적이지 않습니다.")
            # self.add_error('quantity','수량이 입력되지 않았습니다.')

class CancelForm(forms.Form):
    pass
    