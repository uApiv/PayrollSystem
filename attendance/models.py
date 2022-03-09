from django.db import models
from django.contrib.auth.models import User
from projectmanagement.models import Project

# Create your models here.


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="姓名")
    att_date=models.DateField(auto_now_add=False, verbose_name="日期")
    work_time=models.FloatField()
    proj_occ=models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name="参与项目", null=True)

    def get_user_name(self):
        if User.objects.filter(id=self.user.pk).exists():
            name = User.objects.get(id=self.user.pk).username
            return name
        else:
            return None

    def get_proj_name(self):
        if not self.proj_occ:
            return '无项目'
        if Project.objects.filter(pk=self.proj_occ.pk).exists():
            name = Project.objects.get(pk=self.proj_occ.pk).proj_name
            return name
        else:
            return None
