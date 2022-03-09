from django.db import models
from django.contrib.auth.models import User
from user.models import Profile

# Create your models here.


class TrashProfile(models.Model):
    u_name=models.CharField(max_length=30, verbose_name='姓名')
    staff_gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), default='male',
                                    verbose_name='性别')
    staff_age = models.PositiveIntegerField(verbose_name="年龄")
    staff_home = models.CharField(max_length=100, verbose_name="籍贯", null=True)
    staff_nationality = models.CharField(max_length=20, verbose_name="民族", null=True)  # 民族
    staff_tel = models.BigIntegerField(verbose_name="电话")
    start_time = models.DateField(auto_now_add=True, verbose_name="入职时间", null=True)  # 入职时间
    id_card = models.CharField(max_length=20, verbose_name="身份证")  # 身份证号
    staff_type = models.CharField(max_length=100, verbose_name="职位", null=True)  # 职位
    mail_addr = models.CharField(max_length=100, verbose_name="邮寄地址", null=True)
    salary_pre_hour = models.IntegerField(verbose_name="时薪", null=True)  # 时薪
    # staff_id=models.IntegerField(verbose_name='员工ID',)
    std_tax_d = models.FloatField(verbose_name='standard tax deductions', null=True)
    other_d = models.FloatField(verbose_name='other deductions', null=True)
    com_rate = models.FloatField(verbose_name='hourly or commission rate', null=True)
    hour_limit = models.IntegerField(verbose_name="hour limit (some employees may not be able to work overtime)",
                                     null=True)
    salary = models.FloatField(verbose_name='salary (for salaried and commissioned employees)', null=True)
    paycheck_delivery = models.CharField(max_length=100, verbose_name="paycheck delivery method", null=True)
    bank_name = models.CharField(max_length=100, verbose_name="bank name", null=True)
    mail_pay = models.CharField(max_length=100, verbose_name="the address that the paycheck will be mailed to",
                                null=True)
    account = models.CharField(max_length=100, verbose_name="account number", null=True)

    def Set_Attr(self, pro):
        self.staff_gender=pro.staff_gender
        print(pro.mail_addr)
        self.staff_age=pro.staff_age
        self.staff_tel=pro.staff_tel
        self.start_time=pro.start_time
        self.id_card=pro.id_card
        self.staff_type=pro.staff_type
        self.mail_addr=pro.mail_addr
        self.salary_pre_hour=pro.salary_pre_hour
        self.std_tax_d=pro.std_tax_d
        self.other_d=pro.other_d
        self.com_rate=pro.com_rate
        self.hour_limit=pro.hour_limit
        self.salary=pro.salary
        self.paycheck_delivery=pro.paycheck_delivery
        self.bank_name=pro.bank_name
        self.mail_pay=pro.mail_pay
        self.account=pro.account