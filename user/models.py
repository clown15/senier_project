from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(models.Model):
    email = models.EmailField(primary_key=True,verbose_name="이메일")
    password = models.CharField(max_length=128,verbose_name="비밀번호")
    level = models.CharField(max_length=16,verbose_name="등급",choices = (
        ("admin","관리자"),
        ("user","고객"),
    ),default="user")
    creation_date = models.DateTimeField(auto_now_add=True,verbose_name="등록일")

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

class Allergy(models.Model):
    # 알러지 정보
    # 메밀, 밀, 대두, 땅콩, 호두, 잣, 복숭아, 토마토, 우유, 새우, 고등어, 오징어, 게, 조개, 돼지고기, 쇠고기, 닭고기
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    buckwheat = models.BooleanField(default = False, verbose_name="메밀")
    wheat = models.BooleanField(default = False, verbose_name="밀")
    Big_head = models.BooleanField(default = False, verbose_name="대두")
    peanut = models.BooleanField(default = False, verbose_name="땅콩")
    Walnut = models.BooleanField(default = False, verbose_name="호두")
    pine_nut = models.BooleanField(default = False, verbose_name="잣")
    peach = models.BooleanField(default = False, verbose_name="복숭아")
    tomato = models.BooleanField(default = False, verbose_name="토마토")
    milk = models.BooleanField(default = False, verbose_name="우유")
    shrimp = models.BooleanField(default = False, verbose_name="새우")
    Mackerel = models.BooleanField(default = False, verbose_name="고등어")
    squid = models.BooleanField(default = False, verbose_name="오징어")
    crab = models.BooleanField(default = False, verbose_name="게")
    clam = models.BooleanField(default = False, verbose_name="조개")
    Pork = models.BooleanField(default = False, verbose_name="돼지고기")
    beef = models.BooleanField(default = False, verbose_name="쇠고기")
    chicken = models.BooleanField(default = False, verbose_name="닭고기")

    class Meta:
        db_table = "user_allergy"
        verbose_name = "사용자 알러지"
        verbose_name_plural = "사용자 알러지"

class AllergyLevel(models.IntegerChoices):
    NONE = 0, _('None')
    LOW = 1, _('Low')
    HIGH = 2, _('High')


class DegreeOfAllergy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자", related_name="allergy_level")
    buckwheat = models.IntegerField(default=AllergyLevel.NONE, verbose_name="메밀", choices=AllergyLevel.choices)
    wheat = models.IntegerField(default = AllergyLevel.NONE, verbose_name="밀", choices=AllergyLevel.choices)
    Big_head = models.IntegerField(default = AllergyLevel.NONE, verbose_name="대두", choices=AllergyLevel.choices)
    peanut = models.IntegerField(default = AllergyLevel.NONE, verbose_name="땅콩", choices=AllergyLevel.choices)
    Walnut = models.IntegerField(default = AllergyLevel.NONE, verbose_name="호두", choices=AllergyLevel.choices)
    pine_nut = models.IntegerField(default = AllergyLevel.NONE, verbose_name="잣", choices=AllergyLevel.choices)
    peach = models.IntegerField(default = AllergyLevel.NONE, verbose_name="복숭아", choices=AllergyLevel.choices)
    tomato = models.IntegerField(default = AllergyLevel.NONE, verbose_name="토마토", choices=AllergyLevel.choices)
    milk = models.IntegerField(default = AllergyLevel.NONE, verbose_name="우유", choices=AllergyLevel.choices)
    shrimp = models.IntegerField(default = AllergyLevel.NONE, verbose_name="새우", choices=AllergyLevel.choices)
    Mackerel = models.IntegerField(default = AllergyLevel.NONE, verbose_name="고등어", choices=AllergyLevel.choices)
    squid = models.IntegerField(default = AllergyLevel.NONE, verbose_name="오징어", choices=AllergyLevel.choices)
    crab = models.IntegerField(default = AllergyLevel.NONE, verbose_name="게", choices=AllergyLevel.choices)
    clam = models.IntegerField(default = AllergyLevel.NONE, verbose_name="조개", choices=AllergyLevel.choices)
    Pork = models.IntegerField(default = AllergyLevel.NONE, verbose_name="돼지고기", choices=AllergyLevel.choices)
    beef = models.IntegerField(default = AllergyLevel.NONE, verbose_name="쇠고기", choices=AllergyLevel.choices)
    chicken = models.IntegerField(default = AllergyLevel.NONE, verbose_name="닭고기", choices=AllergyLevel.choices)

    class Meta:
        db_table = "user_degree_of_allergy"
        verbose_name = "사용자 알러지 정도"
        verbose_name_plural = "사용자 알러지 정도"