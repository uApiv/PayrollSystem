from django.urls import reverse
from django.shortcuts import render,get_object_or_404, redirect
from .forms import TimecardForm
from .models import Attendance
from projectmanagement.models import Project
from django.http.response import HttpResponse, JsonResponse

# Create your views here.

def att_list(request):
    usr = request.user
    if usr.is_authenticated:
        if usr.get_staff_type() != '管理员':
            att_list = Attendance.objects.filter(user=usr)
        else:
            att_list = Attendance.objects.all()
        context = {}
        context['att_list'] = att_list
        return render(request, 'att_list.html', context)
    else:
        return redirect(reverse('login'))


def view_timecard(request):
    usr = request.user
    timecard_form = TimecardForm()
    if usr.is_authenticated:
        if request.method == 'POST':
            timecard_form = TimecardForm(request.POST)
            # print(usermodify_form)
            if timecard_form.is_valid():
                # print(timecard_form.cleaned_data)
                # att_date = timecard_form.cleaned_data['att_date']
                att = Attendance.objects.filter(user=usr, att_date=timecard_form.cleaned_data['att_date'])
                if len(att)==0:
                    att=Attendance()
                    att.att_date=timecard_form.cleaned_data['att_date']
                    att.user=usr
                elif len(att)==1:
                    att=att[0]
                else:
                    att = att[0]
                    print('WRONG IN view_timecard at att')
                att.work_time = timecard_form.cleaned_data['work_time']
                if timecard_form.cleaned_data['proj_occ']=='不选择项目':
                    att.proj_occ=None
                else:
                    att.proj_occ = Project.objects.filter(proj_name=timecard_form.cleaned_data['proj_occ'])[0]
                print(att.proj_occ)
                # proj=Project.objects.filter(proj_name=att.proj_occ)
                # print(proj[0])
                # add1 = Attendance(user=usr, att_date=att_date, work_time=work_time, proj_occ=proj[0])
                print('111111111111111111111111111111')
                att.save()

                return redirect(reverse('att_list'))
        # usermodify_form = UserAppendForm()
        context = {}
        context['timecard_form'] = timecard_form
        return render(request, 'view_timecard.html', context)
    else:
        return redirect(reverse('login'))

def ajax_on_change_tcf(request):
    print(request.POST['time'])
    str_time=request.POST['time']
    atts=Attendance.objects.filter(user=request.user, att_date=str_time)
    if len(atts) == 0:
        return JsonResponse({'msg': 'no result'})
    elif len(atts) == 1:
        return JsonResponse({'msg': '1 result', 'work_time':atts[0].work_time, 'proj_occ':atts[0].get_proj_name()})
    else:
        return JsonResponse({'msg':'wrong'})