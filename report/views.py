from django.shortcuts import render
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from .forms import SelForm
from attendance.models import Attendance
from django.contrib.auth.models import User
import datetime
from orders.models import Orders
from .forms import EmpForm, EmpResForm
from django.http.response import JsonResponse

# Create your views here.

def admin_report(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            selform = SelForm(request.POST)
            if selform.is_valid():
                start_date=selform.cleaned_data['start_date']
                end_date = selform.cleaned_data['end_date']
                emp_names = selform.cleaned_data['emp_names']
                emp_names = emp_names.split('/')
                res=[]
                for e in emp_names:
                    if len(User.objects.filter(username=e)) == 0:
                        continue
                    e_usr=User.objects.filter(username=e)[0]
                    toth=sum([att.work_time for att in Attendance.objects.filter(user=e_usr, att_date__range=(start_date, end_date))])
                    tot_sal=0.0
                    if e_usr.get_staff_type() == '小时工':
                        # print(last_date.last_run_date)
                        # print(type(last_date.last_run_date))
                        sph = e_usr.get_salary_pre_hour()
                        atts = Attendance.objects.filter(user=e_usr, att_date__range=(
                        start_date, end_date))
                        toth = 0.0
                        for att in atts:
                            toth += att.work_time
                        tot_sal = toth * sph
                        # print(r['salary'])
                    elif e_usr.get_staff_type() == '受薪雇员':
                        sal = e_usr.get_user_profile().salary
                        atts = Attendance.objects.filter(user=e_usr,
                                                         att_date__range=(
                                                         start_date, end_date))
                        tot_sal = len(atts) / 30 * sal
                    elif e_usr.get_staff_type() == '委托员工':
                        sal = e_usr.get_user_profile().salary
                        atts = Attendance.objects.filter(user=e_usr,
                                                         att_date__range=(
                                                         start_date, end_date))
                        ords = Orders.objects.filter(creator=e_usr)
                        tot_o_val = sum([o.order_total_price for o in ords])
                        tot_sal = len(atts) / 30 * sal + tot_o_val * e_usr.get_user_profile().com_rate
                    else:
                        print(e_usr.get_staff_type())
                    res.append({'name':e, 'tot_time':toth, 'tot_sal':tot_sal})
                return render(request, 'admin_report.html', {'res': res})
            else:
                return render(request, 'sel_rep_meth.html', {'selform': selform})
        else:
            selform=SelForm()

            return render(request, 'sel_rep_meth.html', {'selform':selform})
    else:
        return redirect(reverse('login'))


def employee_report(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            start_date = request.POST['st_date']
            end_date = request.POST['ed_date']
            if request.POST['proj_occ'] == '不选择项目':
                toth=sum([att.work_time for att in Attendance.objects.filter(user=user, att_date__range=(start_date, end_date))])
            else:
                toth=sum([att.work_time for att in Attendance.objects.filter(user=user, att_date__range=(start_date, end_date),
                                                                             proj_occ__proj_name=request.POST['proj_occ'])])
            tot_sal = 0.0
            if user.get_staff_type() == '小时工':
                # print(last_date.last_run_date)
                # print(type(last_date.last_run_date))
                sph = user.get_salary_pre_hour()
                atts = Attendance.objects.filter(user=user, att_date__range=(
                    start_date, end_date))
                toth = 0.0
                for att in atts:
                    toth += att.work_time
                tot_sal = toth * sph
                # print(r['salary'])
            elif user.get_staff_type() == '受薪雇员':
                sal = user.get_user_profile().salary
                atts = Attendance.objects.filter(user=user,
                                                 att_date__range=(
                                                     start_date, end_date))
                tot_sal = len(atts) / 30 * sal
            elif user.get_staff_type() == '委托员工':
                sal = user.get_user_profile().salary
                atts = Attendance.objects.filter(user=user,
                                                 att_date__range=(
                                                     start_date, end_date))
                ords = Orders.objects.filter(creator=user)
                tot_o_val = sum([o.order_total_price for o in ords])
                tot_sal = len(atts) / 30 * sal + tot_o_val * user.get_user_profile().com_rate
            else:
                print(user.get_staff_type())

            return JsonResponse({'toth': toth, 'tot_sal': tot_sal})
        else:
            empresform = EmpResForm()
            return render(request, 'emp_report.html', {'empform':EmpForm(), 'empresform':empresform})
    else:
        return redirect(reverse('login'))