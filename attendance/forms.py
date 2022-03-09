from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import widgets
from projectmanagement.models import Project



class TimecardForm(forms.Form):
    ps = Project.objects.all()
    proj = [('不选择项目', '不选择项目')]
    for p in ps:
        proj.append((p.proj_name, p.proj_name))
    att_date = forms.DateField(
        label='选择日期',
        # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入交货时间'})
        widget=forms.DateInput(attrs={'type': 'date', 'onchange':'on_change_tcf()'})
    )

    work_time = forms.FloatField(
        label='工作时长',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入工作时长'})
    )

    proj_occ = forms.CharField(
        label='项目名称',
        widget=forms.Select(choices=proj),
    )
