from django.db import models

# Create your models here.

class sys_run_date(models.Model):
    last_run_date=models.DateField(verbose_name='上次运行时间')