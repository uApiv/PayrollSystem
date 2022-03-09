from django.shortcuts import render
from .models import Project
from .forms import ProjInfoForm
from django.urls import reverse
from django.shortcuts import render,get_object_or_404, redirect

# Create your views here.

def project_list(request):
    projs = Project.objects.all()
    context = {}
    context['projs'] = projs
    return render(request, 'proj_list.html', context)

def project_append(request):
    usr = request.user
    proj_app_form = ProjInfoForm()
    if usr.is_authenticated:
        if request.method == 'POST':
            proj_app_form = ProjInfoForm(request.POST)
            # print(usermodify_form)
            if proj_app_form.is_valid():
                print(proj_app_form.cleaned_data)
                projname = proj_app_form.cleaned_data['proj_name']
                projval = proj_app_form.cleaned_data['proj_value']
                add1 = Project(proj_name=projname, proj_value=projval)
                add1.save()

                return redirect(reverse('project_list'))
        # usermodify_form = UserAppendForm()
        context = {}
        context['proj_app_form'] = proj_app_form
        return render(request, 'proj_append.html', context)
    else:
        return redirect(reverse('login'))

def project_modify(request, proj_pk):
    usr = request.user
    if usr.is_authenticated:
        pro = Project.objects.get(pk=proj_pk)
        if request.method == 'POST':
            projmodify_form = ProjInfoForm(request.POST)
            if projmodify_form.is_valid():
                pro.proj_name = projmodify_form.cleaned_data['proj_name']
                pro.proj_value = projmodify_form.cleaned_data['proj_value']
                pro.save()
                return redirect(reverse('project_list'))
        # user.get_staff_type
        projmodify_form = ProjInfoForm(initial={'proj_name': pro.proj_name, 'proj_value': pro.proj_value})
        # print(usermodify_form)
        context = {}
        context['projmodify_form'] = projmodify_form
        # context['user_type'] = user.get_staff_type()
        return render(request, 'proj_modify.html', context)
    else:
        return redirect(reverse('login'))

def project_delete(request, proj_pk):
    user = request.user
    if user.is_authenticated:
        Project.objects.get(pk=proj_pk).delete()
        return redirect(reverse('project_list'))
    else:
        return redirect(reverse('login'))