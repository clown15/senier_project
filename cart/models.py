from django.db import models

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey("user.User",on_delete=models.CASCADE,verbose_name="주문자", related_name="cart_orderer")
    product = models.ForeignKey("product.Product",on_delete=models.CASCADE,verbose_name="상품")
    seller = models.ForeignKey("user.User",on_delete=models.CASCADE,verbose_name="판매자", related_name="cart_seller")
    quantity = models.IntegerField(verbose_name="수량")
    total_price = models.IntegerField(verbose_name="가격")
    status = models.CharField(max_length=30, verbose_name="상태", choices = (
        ("waiting","대기"),
        ("cancel","취소"),
        ("finish","종료"),
    ), default="waiting")
    creation_date = models.DateTimeField(auto_now_add=True,verbose_name="등록일")

    # admin 페이지에서 값을 추가하면서 객체를 불러올때 문자열로 보여주기 위함
    def __str__(self):
        return str(self.user)+' '+str(self.product)

    class Meta:
        db_table = "cart"
        verbose_name = "장바구니"
        verbose_name_plural = "장바구니"