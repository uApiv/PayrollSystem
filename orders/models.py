from django.db import models
from django.contrib.auth.models import User

class Orders(models.Model):#订单
    creator=models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="创建者")
    # order_name=models.ForeignKey(Product,on_delete=models.DO_NOTHING, verbose_name="产品名称")
    order_name = models.CharField(max_length=100, verbose_name="产品名称")
    order_client=models.CharField(max_length=100, verbose_name="客户名称")
    order_poc = models.CharField(max_length=100, verbose_name="客户联络点", null=True)
    order_bill_addr = models.CharField(max_length=100, verbose_name="客户账单地址", null=True)
    order_number = models.IntegerField(verbose_name="数量")
    order_price=models.IntegerField(verbose_name="单价(元)")
    order_total_price = models.IntegerField(verbose_name="总价(元)")
    order_time = models.DateField(verbose_name="订货时间")
    order_end = models.DateField(verbose_name="交货时间")
    order_supplement=models.TextField(verbose_name="补充", null=True, blank=True)

    class Meta:
        ordering = ['-order_time']
