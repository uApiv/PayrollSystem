from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import widgets
from projectmanagement.models import Project


class SelForm(forms.Form):

    report_type = forms.CharField(
        label='选择日期',
        # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入交货时间'})
        widget=forms.Select(choices=[('工作总时长', '工作总时长'), ('工资支付情况', '工资支付情况')])
    )

    start_date = forms.DateField(
        label='选择开始日期',
        # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入交货时间'})
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    end_date = forms.DateField(
        label='选择截止日期',
        # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入交货时间'})
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    emp_names = forms.CharField(
        label='员工姓名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入员工姓名，多个员工用/分开'})
    )

class EmpForm(forms.Form):
    ps = Project.objects.all()
    proj = [('不选择项目', '不选择项目')]
    for p in ps:
        proj.append((p.proj_name, p.proj_name))
    report_type = forms.CharField(
        label='选择查询',
        # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入交货时间'})
        widget=forms.Select(choices=[('工作总时长', '工作总时长'), ('工资支付情况', '工资支付情况')])
    )

    start_date = forms.DateField(
        label='选择开始日期',
        # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入交货时间'})
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    end_date = forms.DateField(
        label='选择截止日期',
        # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入交货时间'})
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    proj_occ = forms.CharField(
        label='项目名称',
        widget=forms.Select(choices=proj),
    )

class EmpResForm(forms.Form):
    toth = forms.FloatField(
        label='工作总时长',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    tosal = forms.FloatField(
        label='工资支付金额',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )