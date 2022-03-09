from django.db import models

# Create your models here.

class Project(models.Model):
    proj_name=models.CharField(max_length=10, verbose_name='项目名', unique=True)
    proj_value=models.FloatField(verbose_name='项目金额')
