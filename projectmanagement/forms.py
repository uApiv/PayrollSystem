from django import forms
from django.forms import widgets


class ProjInfoForm(forms.Form):
    proj_name=forms.CharField(
        label='项目名称',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入项目名称'})
    )
    proj_value = forms.FloatField(
        label='项目金额',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入项目金额'})
    )