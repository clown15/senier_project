from django.db import models

# Create your models here.
class Order(models.Model):
    orderer = models.ForeignKey("user.User",on_delete=models.CASCADE,verbose_name="주문자", related_name="orderer")
    product = models.ForeignKey("product.Product",on_delete=models.CASCADE,verbose_name="상품")
    seller = models.ForeignKey("user.User",on_delete=models.CASCADE,verbose_name="판매자", related_name="seller")
    quantity = models.IntegerField(verbose_name="수량")
    total_price = models.IntegerField(verbose_name="가격")
    rate = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="평점", default=0)
    creation_date = models.DateTimeField(auto_now_add=True,verbose_name="등록일")

    # admin 페이지에서 값을 추가하면서 객체를 불러올때 문자열로 보여주기 위함
    def __str__(self):
        return str(self.orderer)+' '+str(self.product)

    class Meta:
        db_table = "order"
        verbose_name = "주문"
        verbose_name_plural = "주문"