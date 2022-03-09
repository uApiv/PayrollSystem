from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import sys_run_date
import datetime
from attendance.models import Attendance
from orders.models import Orders
from bank.bank import Bank

# Create your views here.

def payroll_view(request):
    user = request.user
    if user.is_authenticated:
        users=User.objects.all()
        res=[{'usr':u, 'name':u.username, 'paycheck_delivery':u.get_user_profile().paycheck_delivery, 'salary':0}
             for u in users if u.get_staff_type()!='管理员']
        # print(res)
        last_date = sys_run_date.objects.all()
        if len(last_date) == 1:
            last_date = last_date[0]
        else:
            print('WRONG IN PAYROLL_VIEW 1')
            last_date = datetime.date.today()
        for r in res:
            if r['usr'].get_staff_type()=='小时工':
                # print(last_date.last_run_date)
                # print(type(last_date.last_run_date))
                sph=r['usr'].get_salary_pre_hour()
                atts=Attendance.objects.filter(user=r['usr'], att_date__range=(last_date.last_run_date, datetime.date.today()))
                toth=0.0
                for att in atts:
                    toth+=att.work_time
                r['salary']=toth*sph
                # print(r['salary'])
            elif r['usr'].get_staff_type()=='受薪雇员':
                sal=r['usr'].get_user_profile().salary
                atts = Attendance.objects.filter(user=r['usr'],
                                                 att_date__range=(last_date.last_run_date, datetime.date.today()))
                r['salary']=len(atts)/30*sal
            elif r['usr'].get_staff_type() == '委托员工':
                sal = r['usr'].get_user_profile().salary
                atts = Attendance.objects.filter(user=r['usr'],
                                                 att_date__range=(last_date.last_run_date, datetime.date.today()))
                ords=Orders.objects.filter(creator=r['usr'])
                tot_o_val=sum([o.order_total_price for o in ords])
                r['salary'] = len(atts) / 30 * sal+tot_o_val*r['usr'].get_user_profile().com_rate
            else:
                print(r['usr'].get_staff_type())
        return render(request, 'payroll_view.html', {'res':res})
    else:
        return redirect(reverse('login'))

def get_acc_sal(usr):
    last_date = sys_run_date.objects.all()
    if len(last_date) == 1:
        last_date = last_date[0]
    else:
        print('WRONG IN PAYROLL_VIEW 1')
        last_date = datetime.date.today()
    tot_sal=0.0
    if usr.get_staff_type() == '小时工':
        # print(last_date.last_run_date)
        # print(type(last_date.last_run_date))
        sph = usr.get_salary_pre_hour()
        atts = Attendance.objects.filter(user=usr,
                                         att_date__range=(last_date.last_run_date, datetime.date.today()))
        toth = 0.0
        for att in atts:
            toth += att.work_time
        tot_sal = toth * sph
        # print(r['salary'])
    elif usr.get_staff_type() == '受薪雇员':
        sal = usr.get_user_profile().salary
        atts = Attendance.objects.filter(user=usr,
                                         att_date__range=(last_date.last_run_date, datetime.date.today()))
        tot_sal = len(atts) / 30 * sal
    elif usr.get_staff_type() == '委托员工':
        sal = usr.get_user_profile().salary
        atts = Attendance.objects.filter(user=usr,
                                         att_date__range=(last_date.last_run_date, datetime.date.today()))
        ords = Orders.objects.filter(creator=usr)
        tot_o_val = sum([o.order_total_price for o in ords])
        tot_sal = len(atts) / 30 * sal + tot_o_val * usr.get_user_profile().com_rate
    else:
        print(usr.get_staff_type())
    return {'acc':usr.get_user_profile().account, 'tot_sal':tot_sal}

def run_payroll(request):
    user = request.user
    # print('OOOOO')
    if user.is_authenticated:

        users = User.objects.all()
        res = [{'usr':u, 'account': u.get_user_profile().account, 'salary': 0}
               for u in users if u.get_user_profile().paycheck_delivery == '存入银行']
        # print(res)
        last_date = sys_run_date.objects.all()
        if len(last_date) == 1:
            last_date = last_date[0]
        else:
            print('WRONG IN PAYROLL_VIEW 1')
            last_date = datetime.date.today()
        for r in res:
            # if r['usr'].get_staff_type() == '小时工':
            #     # print(last_date.last_run_date)
            #     # print(type(last_date.last_run_date))
            #     sph = r['usr'].get_salary_pre_hour()
            #     atts = Attendance.objects.filter(user=r['usr'],
            #                                      att_date__range=(last_date.last_run_date, datetime.date.today()))
            #     toth = 0.0
            #     for att in atts:
            #         toth += att.work_time
            #     r['salary'] = toth * sph
            #     # print(r['salary'])
            # elif r['usr'].get_staff_type() == '受薪雇员':
            #     sal = r['usr'].get_user_profile().salary
            #     atts = Attendance.objects.filter(user=r['usr'],
            #                                      att_date__range=(last_date.last_run_date, datetime.date.today()))
            #     r['salary'] = len(atts) / 30 * sal
            # elif r['usr'].get_staff_type() == '委托员工':
            #     sal = r['usr'].get_user_profile().salary
            #     atts = Attendance.objects.filter(user=r['usr'],
            #                                      att_date__range=(last_date.last_run_date, datetime.date.today()))
            #     ords = Orders.objects.filter(creator=r['usr'])
            #     tot_o_val = sum([o.order_total_price for o in ords])
            #     r['salary'] = len(atts) / 30 * sal + tot_o_val * r['usr'].get_user_profile().com_rate
            # else:
            #     print(r['usr'].get_staff_type())
            rst=get_acc_sal(r['usr'])
            # print(rst)
            if Bank.Trans_pay(account=rst['acc'], val=rst['tot_sal']):
                continue
            else:
                print('PAY ERROR')
        if len(sys_run_date.objects.all())==0:
            last_date=sys_run_date(last_run_date=datetime.date.today())
        else:
            last_date=sys_run_date.objects.all()[0]
            last_date.last_run_date=datetime.date.today()
        last_date.save()
        return redirect(reverse('payroll_view'))
    else:
        return redirect(reverse('login'))