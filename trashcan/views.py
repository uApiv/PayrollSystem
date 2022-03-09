from django.shortcuts import render, redirect
from .models import TrashProfile
from django.urls import reverse

# Create your views here.


def trash_user_list(request):
    users = TrashProfile.objects.all()
    context = {}
    context['users'] = users
    return render(request, 'trash_user.html', context)

def pro_delete(request, pro_pk):
    user = request.user
    if user.is_authenticated:
        TrashProfile.objects.get(pk=pro_pk).delete()
        return redirect(reverse('trash_user_list'))
    else:
        return redirect(reverse('login'))