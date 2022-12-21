from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=256,verbose_name="상품명")
    price = models.IntegerField(verbose_name="가격")
    category = models.CharField(max_length=30, verbose_name="카테고리", choices =(
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
    ),default="etc")
    info = models.TextField(verbose_name="상품 정보")
    Nutrition_Facts = models.ImageField(upload_to='images', blank=True, null=True, verbose_name="영양 정보")
    creator = models.ForeignKey("user.User",on_delete=models.CASCADE, verbose_name="생성자")
    creation_date = models.DateTimeField(auto_now_add=True,verbose_name="등록일")
    sales_rate = models.IntegerField(default = 0, verbose_name="판매량")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product"
        verbose_name = "상품"
        verbose_name_plural = "상품"

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="상품 사진")

    class Meta:
        db_table = "product_image"
        verbose_name = "상품 사진"
        verbose_name_plural = "상품 사진"

class Allergy(models.Model):
    # 알러지 정보
    # 메밀, 밀, 대두, 땅콩, 호두, 잣, 복숭아, 토마토, 우유, 새우, 고등어, 오징어, 게, 조개, 돼지고기, 쇠고기, 닭고기
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품", related_name='allergy')
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
        db_table = "product_allergy"
        verbose_name = "상품 알러지 정보"
        verbose_name_plural = "상품 알러지 정보"

class MetaData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    data = models.TextField(verbose_name="상품 성분 정보")
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE, verbose_name="알러지", related_name='allergy')

    class Meta:
        db_table = "product_meta_data"
        verbose_name = "상품 메타데이터"
        verbose_name_plural = "상품 메타데이터"