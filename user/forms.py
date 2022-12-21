from django import forms
from .models import User
from django.contrib.auth.hashers import check_password

class SignUpForm(forms.Form):
    email = forms.EmailField(
        error_messages = {
            'required':'이메일을 입력하세요.'
        },
        label = "이메일",
    )
    password = forms.CharField(
        error_messages = {
            'required':'비밀번호를 입력하세요.'
        },
        widget = forms.PasswordInput,
        label = "비밀번호",
    )
    re_password = forms.CharField(
        error_messages = {
            'required':'비밀번호를 입력하세요.'
        },
        widget = forms.PasswordInput,
        label = "비밀번호 확인",
    )
    level = forms.ChoiceField(
        error_messages = {
            'required':'등급을 선택하세요.'
        },
        choices = (
            # (실제 값, 보여지는 값)
            ("admin","관리자"),
            ("user","고객"),
        ),
        # 초기값 설정
        initial = "user",
        label = "등급",
    )

    # level = forms.CharField(
    #     widget=forms.Select(choices=(
            # ("admin","관리자"),
            # ("user","고객"),
        # )),
    # )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        level = cleaned_data.get('level')

        if User.objects.filter(email=email).exists():
            self.add_error('email','가입정보가 존재합니다.')
        # 두 값이 있는지 확인 후 값이 같은지 확인
        if password and re_password:
            if password != re_password:
                self.add_error('password','비밀번호가 다릅니다.')
                self.add_error('re_password','비밀번호가 다릅니다.')

class AllergyForm(SignUpForm):
    buckwheat = forms.BooleanField(
        label = "메밀",
        required = False,
    )
    wheat = forms.BooleanField(
        label = "밀",
        required = False,
    )
    Big_head = forms.BooleanField(
        label = "대두",
        required = False,
    )
    peanut = forms.BooleanField(
        label = "땅콩",
        required = False,
    )
    Walnut = forms.BooleanField(
        label = "호두",
        required = False,
    )
    pine_nut = forms.BooleanField(
        label = "잣",
        required = False,
    )
    peach = forms.BooleanField(
        label = "복숭아",
        required = False,
    )
    tomato = forms.BooleanField(
        label = "토마토",
        required = False,
    )
    milk = forms.BooleanField(
        label = "우유",
        required = False,
    )
    shrimp = forms.BooleanField(
        label = "새우",
        required = False,
    )
    Mackerel = forms.BooleanField(
        label = "고등어",
        required = False,
    )
    squid = forms.BooleanField(
        label = "오징어",
        required = False,
    )
    crab = forms.BooleanField(
        label = "게",
        required = False,
    )
    clam = forms.BooleanField(
        label = "조개",
        required = False,
    )
    Pork = forms.BooleanField(
        label = "돼지고기",
        required = False,
    )
    beef = forms.BooleanField(
        label = "쇠고기",
        required = False,
    )
    chicken = forms.BooleanField(
        label = "닭고기",
        required = False,
    )

class AllergyLevelForm(SignUpForm):
    CHOICES=[
        (0,'없음'),
        (1,'약간 있음'),
        (2,'심함'),
    ]

    buckwheat = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "메밀",
        required = False,
    )
    wheat = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "밀",
        required = False,
    )
    Big_head = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "대두",
        required = False,
    )
    peanut = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "땅콩",
        required = False,
    )
    Walnut = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "호두",
        required = False,
    )
    pine_nut = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "잣",
        required = False,
    )
    peach = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "복숭아",
        required = False,
    )
    tomato = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "토마토",
        required = False,
    )
    milk = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "우유",
        required = False,
    )
    shrimp = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "새우",
        required = False,
    )
    Mackerel = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "고등어",
        required = False,
    )
    squid = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "오징어",
        required = False,
    )
    crab = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "게",
        required = False,
    )
    clam = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "조개",
        required = False,
    )
    Pork = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "돼지고기",
        required = False,
    )
    beef = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "쇠고기",
        required = False,
    )
    chicken = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label = "닭고기",
        required = False,
    )

class SignInForm(forms.Form):
    email = forms.EmailField(
        error_messages = {
            'required':'이메일을 입력하세요.'
        },
        label = "이메일",
    )
    password = forms.CharField(
        error_messages = {
            'required':'비밀번호를 입력하세요.'
        },
        widget = forms.PasswordInput,
        label = "비밀번호",
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)

            if not check_password(password,user.password):
                self.add_error('password','비밀번호가 다릅니다.')
        
        except User.DoesNotExist:
            self.add_error("email","아이디가 존재하지 않습니다.")