from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import LoginForm, UserAppendForm, ChangePasswordForm, StaffTypeForm, UserModifyForm, AttendenceForm,\
    UserSelectForm, AttendenceSelectForm, SalarySelectForm, UserNormalSelectForm, AttendenceNormalSelectForm,SalaryNormalSelectForm,PayMethodForm
from django.contrib import auth
from .models import Salary,Profile,Position
from django.db.models import Q
import time
import payroll.views as pv
from bank.bank import Bank
from trashcan.models import TrashProfile

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            print(user.groups)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context = {}
    return render(request, 'user_info.html', context)

def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def user_list(request):
    users = User.objects.all()
    context = {}
    context['users'] = users
    return render(request, 'user_list.html', context)


# def attendence_lists(request):
#     attendence_lists = Attendance.objects.all()
#     # for a in attendence_lists:
#     #     print(str(a.start_time)[11:16])
#     context = {}
#     context['attendence_lists'] = attendence_lists
#     return render(request, 'attendence_lists.html', context)
#
#
# def attendence_list(request, user_pk):
#     ur =get_object_or_404(User,pk=user_pk)
#     attendence_lists =Attendance.objects.filter(staff_name= ur)
#     context = {}
#     context['attendence_lists'] = attendence_lists
#     return render(request, 'attendence_list.html', context)

def salary_lists(request):
    salary_lists = Salary.objects.all()
    context = {}
    context['salary_lists'] = salary_lists
    return render(request, 'salary_lists.html', context)

def salary_list(request,user_pk):
    ur =get_object_or_404(User,pk=user_pk)
    salary_lists =Salary.objects.filter(staff_name= ur)
    context = {}
    context['salary_lists'] = salary_lists
    return render(request, 'salary_list.html', context)


def apply(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            apply_form = LoginForm(request.POST)
            if apply_form.is_valid():
                return redirect(request.GET.get('from', reverse('home')))
        else:
            apply_form = LoginForm()

        context = {}
        context['apply_form'] = apply_form
        return render(request, 'apply.html', context)
    else:
        return redirect(reverse('login'))


def user_delete(request, user_pk):
    #验证当前用户的登录状态
    user = request.user
    if user.is_authenticated:
        usr=User.objects.get(pk=user_pk)
        rst = pv.get_acc_sal(usr)
        # print(rst)
        if Bank.Trans_pay(account=rst['acc'], val=rst['tot_sal']):
            print('PAY COMPLETE')
        else:
            print('PAY ERROR')
        tp=TrashProfile()
        tp.u_name=usr.username
        print(Profile.objects.filter(user=usr)[0].mail_addr)
        tp.Set_Attr(Profile.objects.filter(user=usr)[0])
        # print(tp.mail_addr)
        tp.save()
        usr.delete()
        return redirect(reverse('user_list'))
    else:
        return redirect(reverse('login'))

def usermodify(request,user_pk):
    usr = request.user
    if usr.is_authenticated:
        user =get_object_or_404(User, pk=user_pk)
        if user.get_staff_gender() == '男':
            tem_gender = 'male'
        else:
            tem_gender = 'female'
        pro = Profile.objects.get(user=user)
        if request.method == 'POST':
            usermodify_form = UserModifyForm(request.POST)
            if usermodify_form.is_valid():
                user.username = usermodify_form.cleaned_data['username']

                # user.groups=auth.models.Group(name=usermodify_form.cleaned_data['type'])
                # user.groups.add(auth.models.Group(name=usermodify_form.cleaned_data['type']))
                # print(usermodify_form.cleaned_data['type'])
                pro.staff_type = usermodify_form.cleaned_data['type']
                pro.staff_gender = usermodify_form.cleaned_data['gender']
                pro.staff_age = usermodify_form.cleaned_data['age']
                # pro.staff_home = usermodify_form.cleaned_data['home']
                # pro.staff_nationality = usermodify_form.cleaned_data['nationality']
                pro.staff_tel = usermodify_form.cleaned_data['phone']
                pro.id_card = usermodify_form.cleaned_data['id_card']
                pro.salary_pre_hour = usermodify_form.cleaned_data['salary_pre_hour']
                pro.mail_addr = usermodify_form.cleaned_data['mail_addr']
                pro.std_tax_d = usermodify_form.cleaned_data['std_tax_d']
                pro.other_d = usermodify_form.cleaned_data['other_d']
                pro.salary = usermodify_form.cleaned_data['salary']
                pro.com_rate = usermodify_form.cleaned_data['com_rate']
                pro.hour_limit = usermodify_form.cleaned_data['hour_limit']
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!', com_rate)
                if pro.com_rate:
                    pro.com_rate = float(pro.com_rate[-2:]) / 100
                else:
                    pro.com_rate = None

                if usermodify_form.cleaned_data['password']:
                    user.set_password(usermodify_form.cleaned_data['password'])
                user.save()
                pro.save()
                return redirect(reverse('user_list'))
        # user.get_staff_type
        usermodify_form = UserModifyForm(initial={'username':user.username, 'type':user.get_staff_type, 'mail_addr':user.get_user_profile().mail_addr,
                                                   'gender':tem_gender,'age':user.get_staff_age,
                                                   'phone':user.get_staff_tel, 'id_card':user.get_id_card,
                                                   'salary_pre_hour':user.get_salary_pre_hour, 'salary':user.get_user_profile().salary,
                                                  'com_rate':user.get_user_profile().com_rate, 'std_tax_d':user.get_user_profile().std_tax_d,
                                                  'other_d':user.get_user_profile().other_d, 'hour_limit': user.get_user_profile().hour_limit,
                                                  'password':user.password})
        print(usermodify_form)
        context = {}
        context['usermodify_form'] = usermodify_form
        context['user_type']=user.get_staff_type()
        return render(request, 'user_modify.html', context)
    else:
        return redirect(reverse('login'))


def userappend(request):
    usr = request.user
    usermodify_form = UserAppendForm()
    if usr.is_authenticated:
        if request.method == 'POST':
            usermodify_form = UserAppendForm(request.POST)
            # print(usermodify_form)
            if usermodify_form.is_valid():
                username = usermodify_form.cleaned_data['username']
                password = usermodify_form.cleaned_data['password']

                print(usermodify_form.cleaned_data['type'])
                if usermodify_form.cleaned_data['type'] == '经理':
                    add = User.objects.create_superuser(username,'', password)
                else:
                    add = User.objects.create_user(username, '',password)
                add.save()
                add.email = str(add.pk) + '@nbt.cn'
                add.save()
                staff_type = usermodify_form.cleaned_data['type']
                staff_gender = usermodify_form.cleaned_data['gender']
                staff_age = usermodify_form.cleaned_data['age']
                # home = usermodify_form.cleaned_data['home']
                # staff_nationality = usermodify_form.cleaned_data['nationality']
                staff_tel = usermodify_form.cleaned_data['phone']
                id_card = usermodify_form.cleaned_data['id_card']
                salary_pre_hour = usermodify_form.cleaned_data['salary_pre_hour']
                mail_addr=usermodify_form.cleaned_data['mail_addr']
                std_tax_d=usermodify_form.cleaned_data['std_tax_d']
                other_d=usermodify_form.cleaned_data['other_d']
                salary=usermodify_form.cleaned_data['salary']
                com_rate=usermodify_form.cleaned_data['com_rate']
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!', com_rate)
                if com_rate:
                    com_rate=float(com_rate[-2:])/100
                else:
                    com_rate=None
                hour_limit=usermodify_form.cleaned_data['hour_limit']
                add1 = Profile(user=add, staff_type=staff_type, mail_addr=mail_addr, staff_gender=staff_gender,
                               staff_age=staff_age, staff_home=None, staff_nationality=None,
                               staff_tel=staff_tel, id_card=id_card, salary_pre_hour=salary_pre_hour, salary=salary,
                               std_tax_d=std_tax_d, other_d=other_d, com_rate=com_rate, hour_limit=hour_limit,
                               paycheck_delivery='pickup')
                add1.save()

                '''print(usermodify_form.cleaned_data['salary_pre_hour'])
                print(usermodify_form.cleaned_data['salary'])
                print(usermodify_form.cleaned_data['com_rate'])'''

                return redirect(reverse('user_list'))
        # usermodify_form = UserAppendForm()
        context = {}
        context['usermodify_form'] = usermodify_form
        return render(request, 'user_append.html', context)
    else:
        return redirect(reverse('login'))

def sel_pay_m(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            pay_form=PayMethodForm(request.POST)
            if pay_form.is_valid():
                pro=Profile.objects.get(user=user)
                pro.paycheck_delivery=pay_form.cleaned_data['method']
                pro.bank_name = pay_form.cleaned_data['bank_name']
                pro.mail_pay = pay_form.cleaned_data['mail']
                pro.account = pay_form.cleaned_data['account']
                pro.save()
                return redirect(reverse('sel_pay_m'))
            else:
                context = {'pay_m_sel_form': pay_form}
                return render(request, 'sel_pay_m.html', context)
        else:
            pro = Profile.objects.get(user=user)
            print(pro.paycheck_delivery)
            pay_form=PayMethodForm(initial={'method':pro.paycheck_delivery, 'mail':pro.mail_pay,
                                            'bank_name':pro.bank_name, 'account':pro.account})
            context = {'pay_m_sel_form': pay_form}
            return render(request, 'sel_pay_m.html', context)
    else:
        return redirect(reverse('login'))


def position_lists(request):
    position_lists = Position.objects.all()
    context = {}
    context['position_lists'] = position_lists
    return render(request, 'staff_type.html', context)


def staff_type_modify(request, position_pk):
    usr = request.user
    if usr.is_authenticated:
        pos = Position.objects.get(pk=position_pk)
        if request.method == 'POST':
            staff_modify_form = StaffTypeForm(request.POST)
            if staff_modify_form.is_valid():
                pos.position =staff_modify_form.cleaned_data['position']
                pos.save()
                return redirect(reverse('position_lists'))

        staff_modify_form = StaffTypeForm(initial={'position':pos.position})
        context = {}
        context['staff_modify_form'] = staff_modify_form
        return render(request, 'staff_type_modify.html', context)
    else:
        return redirect(reverse('login'))

def staff_type_delete(request, position_pk):
    usr = request.user
    if usr.is_authenticated:
        pos = Position.objects.get(pk=position_pk)
        pos.delete()
        return redirect(reverse('position_lists'))
    else:
        return redirect(reverse('login'))


def staff_type_add(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            staff_modify_form = StaffTypeForm(request.POST)
            if staff_modify_form.is_valid():

                pos=Position(position=staff_modify_form.cleaned_data['position'])
                pos.save()
                return redirect(reverse('position_lists'))
        else:
            staff_modify_form = StaffTypeForm
            context = {}
            context['staff_modify_form'] = staff_modify_form
            return render(request, 'staff_type_add.html', context)
    else:
        return redirect(reverse('login'))


# def attendence_append(request):
#     usr = request.user
#     if usr.is_authenticated:
#         if request.method == 'POST':
#             AttendenceForms = AttendenceForm(request.POST)
#             if AttendenceForms.is_valid():
#                 staff_name = AttendenceForms.cleaned_data['staff_name']
#                 user_tem = User.objects.get(username=staff_name)
#                 flag_leave = AttendenceForms.cleaned_data['flag_leave']
#                 flag_business = AttendenceForms.cleaned_data['flag_business']
#                 supplement = AttendenceForms.cleaned_data['supplement']
#                 add = Attendance(staff_name=user_tem, flag_leave=flag_leave,
#                                    flag_business=flag_business, supplement=supplement)
#                 add.save()
#                 return redirect(reverse('attendence_lists'))
#         else:
#             AttendenceForms = AttendenceForm()
#             context = {}
#             context['AttendenceForms'] = AttendenceForms
#             return render(request, 'attendence_form.html', context)
#     else:
#         return redirect(reverse('login'))


# def attendence_delete(request, attendence_pk):
#     usr = request.user
#     if usr.is_authenticated:
#         attendence_tem = Attendance.objects.get(pk=attendence_pk)
#         attendence_tem.delete()
#         return redirect(reverse('attendence_lists'))
#     else:
#         return redirect(reverse('login'))


# def attendence_modify(request, attendence_pk):
#     usr = request.user
#     if usr.is_authenticated:
#         Attendance_tem = Attendance.objects.get(pk=attendence_pk)
#         if request.method == 'POST':
#             AttendenceForms = AttendenceForm(request.POST)
#             if AttendenceForms.is_valid():
#
#                 user_tem = User.objects.get(username=AttendenceForms.cleaned_data['staff_name'])
#                 Attendance_tem.staff_name = user_tem
#                 Attendance_tem.flag_leave = AttendenceForms.cleaned_data['flag_leave']
#                 Attendance_tem.flag_business = AttendenceForms.cleaned_data['flag_business']
#                 Attendance_tem.supplement = AttendenceForms.cleaned_data['supplement']
#
#                 Attendance_tem.save()
#                 return redirect(reverse('attendence_lists'))
#         else:
#             AttendenceForms = AttendenceForm(initial={'staff_name':Attendance_tem.staff_name,'flag_leave':Attendance_tem.flag_leave,
#                                                    'flag_business':Attendance_tem.flag_business,'supplement':Attendance_tem.supplement})
#             context = {}
#             context['AttendenceForms'] = AttendenceForms
#             return render(request, 'attendence_form.html', context)
#     else:
#         return redirect(reverse('login'))


def user_select(request):

    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            UserSelectForms = UserSelectForm(request.POST)
            if UserSelectForms.is_valid():
                keyword = UserSelectForms.cleaned_data['keyword']
                valueword = UserSelectForms.cleaned_data['valueword']
                pro_tem = []
                ans_tem = []
                print(keyword, valueword)
                if keyword == '0':
                    ans_tem = User.objects.filter(id=valueword)
                elif keyword == '1':#姓名
                    ans_tem = User.objects.filter(Q(username__contains=valueword))
                else:
                    if keyword == '2':#职位
                        pro_tem = Profile.objects.filter(staff_type__contains=valueword)
                    if keyword == '3':#性别
                        tem = 'male' if valueword == '男' else 'female'
                        pro_tem = Profile.objects.filter(staff_gender=tem)
                    if keyword == '4':#年龄
                        pro_tem = Profile.objects.filter(staff_age__contains=valueword)
                    if keyword == '5':#籍贯
                        pro_tem = Profile.objects.filter(staff_home__contains=valueword)
                    if keyword == '6':#民族
                        pro_tem = Profile.objects.filter(staff_nationality__contains=valueword)
                    if keyword == '7':#电话
                        pro_tem = Profile.objects.filter(staff_tel__contains=valueword)
                    if keyword == '8':#身份证
                        pro_tem = Profile.objects.filter(id_card__contains=valueword)
                    if keyword == '9':#入职时间
                        pro_tem = Profile.objects.filter(start_time__contains=valueword)
                    if keyword == '10':#时薪
                        pro_tem = Profile.objects.filter(salary_pre_hour=valueword)

                    for p in pro_tem:
                        ans_tem.append(p.user)

                context = {}
                context['users'] = ans_tem
                context['search_res_n'] = len(ans_tem)
                return render(request, 'user_list.html', context)
        else:
            UserSelectForms = UserSelectForm()
            context = {}
            context['UserSelectForms'] = UserSelectForms
            return render(request, 'user_select.html', context)
    else:
        return redirect(reverse('login'))


def user_normal_select(request):

    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            UserNormalSelectForms = UserNormalSelectForm(request.POST)
            if UserNormalSelectForms.is_valid():
                keyword = UserNormalSelectForms.cleaned_data['keyword']
                valueword = UserNormalSelectForms.cleaned_data['valueword']
                pro_tem = []
                ans_tem = []
                print(keyword, valueword)
                if keyword == '1':#姓名
                    ans_tem = User.objects.filter(Q(username__contains=valueword))
                else:
                    if keyword == '2':#职位
                        pro_tem = Profile.objects.filter(staff_type__contains=valueword)
                    if keyword == '3':#性别
                        tem = 'male' if valueword == '男' else 'female'
                        pro_tem = Profile.objects.filter(staff_gender=tem)
                    if keyword == '4':#年龄
                        pro_tem = Profile.objects.filter(staff_age__contains=valueword)
                    if keyword == '5':#籍贯
                        pro_tem = Profile.objects.filter(staff_home__contains=valueword)
                    if keyword == '6':#民族
                        pro_tem = Profile.objects.filter(staff_nationality__contains=valueword)
                    if keyword == '7':#电话
                        pro_tem = Profile.objects.filter(staff_tel__contains=valueword)

                    for p in pro_tem:
                        ans_tem.append(p.user)

                context = {}
                context['users'] = ans_tem
                return render(request, 'user_list.html', context)
        else:
            UserNormalSelectForms = UserNormalSelectForm()
            context = {}
            context['UserNormalSelectForms'] = UserNormalSelectForms
            return render(request, 'user_normal_select.html', context)
    else:
        return redirect(reverse('login'))

# def attendence_select(request):
#
#     usr = request.user
#     if usr.is_authenticated:
#         if request.method == 'POST':
#             if usr.get_staff_type() == '经理':
#                 AttendenceSelectForms = AttendenceSelectForm(request.POST)
#                 if AttendenceSelectForms.is_valid():
#                     keyword = AttendenceSelectForms.cleaned_data['keyword']
#                     valueword = AttendenceSelectForms.cleaned_data['valueword']
#                     ans_tem = []
#                     print(keyword, valueword)
#                     if keyword == '1':#姓名
#                         ans_tem1 = User.objects.filter(Q(username__contains=valueword))
#                         ans_tem = Attendance.objects.filter(staff_name__in=ans_tem1)
#
#                     if keyword == '2':#时间
#                         ans_tem = Attendance.objects.filter(current_time__contains=valueword)
#
#                     context = {}
#                     context['attendence_lists'] = ans_tem
#                     return render(request, 'attendence_lists.html', context)
#             else:
#                 AttendenceNormalSelectForms = AttendenceNormalSelectForm(request.POST)
#                 if AttendenceNormalSelectForms.is_valid():
#                     keyword = AttendenceNormalSelectForms.cleaned_data['keyword']
#                     ans_tem = Attendance.objects.filter(Q(current_time__contains=keyword),Q(staff_name=usr))
#
#                     context = {}
#                     context['attendence_lists'] = ans_tem
#                     return render(request, 'attendence_list.html', context)
#         else:
#             if usr.get_staff_type() == '经理':
#                 AttendenceSelectForms = AttendenceSelectForm()
#                 context = {}
#                 context['AttendenceSelectForms'] = AttendenceSelectForms
#                 return render(request, 'attendence_select.html', context)
#             else:
#                 AttendenceNormalSelectForms = AttendenceNormalSelectForm()
#                 context = {}
#                 context['AttendenceSelectForms'] = AttendenceNormalSelectForms
#                 return render(request, 'attendence_select.html', context)
#     else:
#         return redirect(reverse('login'))


def salary_select(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            SalarySelectForms = SalarySelectForm(request.POST)
            if SalarySelectForms.is_valid():
                keyword = SalarySelectForms.cleaned_data['keyword']
                valueword = SalarySelectForms.cleaned_data['valueword']
                flag = SalarySelectForms.cleaned_data['flag']
                ans_tem = []
                print(keyword, valueword)
                if keyword == '1':#姓名
                    ans_tem1 = User.objects.filter(Q(username__contains=valueword))
                    ans_tem = Salary.objects.filter(staff_name__in=ans_tem1)

                if keyword == '2':#时间
                    ans_tem = Salary.objects.filter(current_time__contains=valueword)
                if keyword == '3':#出勤
                    if flag == '1':
                        ans_tem = Salary.objects.filter(attend_days=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(attend_days__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(attend_days__lte=valueword)
                if keyword == '4':#请假
                    if flag == '1':
                        ans_tem = Salary.objects.filter(leave_days=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(leave_days__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(leave_days_lte=valueword)
                if keyword == '5':#旷班
                    if flag == '1':
                        ans_tem = Salary.objects.filter(absent_days=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(absent_days__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(absent_days_lte=valueword)
                if keyword == '6':#出差
                    if flag == '1':
                        ans_tem = Salary.objects.filter(business_days=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(business_days__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(business_days_lte=valueword)
                if keyword == '7':#迟到
                    if flag == '1':
                        ans_tem = Salary.objects.filter(late_days=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(late_days__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(late_days_lte=valueword)
                if keyword == '8':#加班时长
                    if flag == '1':
                        ans_tem = Salary.objects.filter(overtime=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(overtime__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(overtime_lte=valueword)
                if keyword == '9':#基础工资
                    if flag == '1':
                        ans_tem = Salary.objects.filter(base_salary=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(base_salary__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(base_salary_lte=valueword)
                if keyword == '10':#加班工资
                    if flag == '1':
                        ans_tem = Salary.objects.filter(overtime_salary=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(overtime_salary__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(overtime_salary_lte=valueword)
                if keyword == '11':#扣款
                    if flag == '1':
                        ans_tem = Salary.objects.filter(kouchu=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(kouchu__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(kouchu_lte=valueword)
                if keyword == '12':#补贴
                    if flag == '1':
                        ans_tem = Salary.objects.filter(allowance=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(allowance__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(allowance_lte=valueword)
                if keyword == '13':#应发
                    if flag == '1':
                        ans_tem = Salary.objects.filter(should_pay=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(should_pay__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(should_pay_lte=valueword)
                if keyword == '14':#所得税
                    if flag == '1':
                        ans_tem = Salary.objects.filter(tax=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(tax__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(tax_lte=valueword)
                if keyword == '15':#实发
                    if flag == '1':
                        ans_tem = Salary.objects.filter(actual_pay=valueword)
                    if flag == '2':
                        ans_tem = Salary.objects.filter(actual_pay__gte=valueword)
                    if flag == '3':
                        ans_tem = Salary.objects.filter(actual_pay_lte=valueword)
                context = {}
                context['salary_lists'] = ans_tem
                return render(request, 'salary_lists.html', context)
        else:
            SalarySelectForms = SalarySelectForm()
            context = {}
            context['SalarySelectForms'] = SalarySelectForms
            return render(request, 'salary_select.html', context)
    else:
        return redirect(reverse('login'))


def salary_normal_select(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            SalaryNormalSelectForms = SalaryNormalSelectForm(request.POST)
            if SalaryNormalSelectForms.is_valid():

                valueword = SalaryNormalSelectForms.cleaned_data['valueword']
                ans_tem = Salary.objects.filter(Q(current_time__contains=valueword),Q(staff_name=usr))
                context = {}
                context['salary_lists'] = ans_tem
                return render(request, 'salary_list.html', context)
        else:
            SalaryNormalSelectForms = SalaryNormalSelectForm()
            context = {}
            context['SalarySelectForms'] = SalaryNormalSelectForms
            return render(request, 'salary_normal_select.html', context)
    else:
        return redirect(reverse('login'))

def leapyear(year):
    if year % 400 == 0:
        return True
    else:
        if year % 4 == 0 and year % 100 != 0:
            return True
    return False


def caculate_salary(request):
    days_1 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_2 = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    users = User.objects.all()
    date = time.strftime('%Y-%m', time.localtime(time.time()))#当前月份 日期
    # if int(date[-2:]) > 1:#一月份的上一个是去年12月
    #     date = date[:-2] + str((int(date[-2:]) - 1))
    # else:
    #     if int(date[3:4]) == 0:#整十年的上一个12月是X9年
    #         date = str(int(str(date[0:4])) - 1) + str(int(date[-2]) - 1)
    #     date = date[:-2] + str(int(date[-2]) - 1)
    # if date[-2] == '-':
    #     date = date[:-1] + '0' + date[-1]
    print(date)
    # attend_tems = Attendance.objects.filter(current_time__contains=date)
    attend_tems=[]
    for user in users:
        salary_pre_hour = user.get_salary_pre_hour()
        attend_days = 0
        leave_days = 0
        absent_days = 0
        business_days=0
        late_days=0
        zaotui_days = 0
        overtime = 0
        base_salary=0
        overtime_salary=0
        kouchu=0
        allowance=0
        should_pay=0
        tax = 0
        actual_pay = 0
        for attend_tem in attend_tems:
            if attend_tem.staff_name == user:
                if attend_tem.flag_leave:#请假
                    leave_days += 1
                else:
                    attend_days += 1
                    if attend_tem.flag_business:#出差
                        business_days += 1
                    else:
                        hour = str(attend_tem.start_time)[11:13]
                        if hour < '23':#迟到
                            late_days += 1
                        hour1 = int(str(attend_tem.start_time)[11:13])
                        if hour1 < 9:#早退
                            zaotui_days += 1
                        else:
                            overtime += (hour1 -1)#加班时长
        if leapyear(int(str(date[0:4]))):
            absent_days += (days_2[int(str(date[-2:]))-1] - attend_days - leave_days)
        else:
            absent_days += (days_1[int(str(date[-2:]))-1] - attend_days - leave_days)
        base_salary += (attend_days * salary_pre_hour)
        kouchu += (absent_days * 100 + late_days * 50 + zaotui_days * 50)
        allowance += (attend_days * 20)
        overtime_salary += (overtime * salary_pre_hour * 2)
        should_pay += (base_salary + allowance + overtime - kouchu)
        if should_pay > 4000:
            tax += int((should_pay - 4000) * 0.1)
        else:
            tax = 0
        actual_pay += (should_pay - tax)
        salary_tem = Salary.objects.filter(Q(current_time__contains=date),Q(staff_name=user))
        if salary_tem:
            salary_tem[0].attend_days = attend_days
            salary_tem[0].leave_days = leave_days
            salary_tem[0].absent_days = absent_days
            salary_tem[0].business_days = business_days
            salary_tem[0].late_days = late_days
            salary_tem[0].zaotui_days = zaotui_days
            salary_tem[0].overtime = overtime
            salary_tem[0].base_salary = base_salary
            salary_tem[0].overtime_salary = overtime_salary
            salary_tem[0].kouchu = kouchu
            salary_tem[0].allowance = allowance
            salary_tem[0].should_pay = should_pay
            salary_tem[0].tax = tax
            salary_tem[0].actual_pay = actual_pay
            salary_tem[0].save()
        else:
            add = Salary(staff_name=user, attend_days=attend_days, leave_days=leave_days, absent_days=absent_days,
                         business_days=business_days, late_days=late_days, zaotui_days=zaotui_days, overtime=overtime,
                         base_salary=base_salary, overtime_salary=overtime_salary, kouchu=kouchu, allowance=allowance,
                         should_pay=should_pay, tax=tax, actual_pay=actual_pay)
            add.save()
    send_mail('Subject', '工资已经发放，请查收.', 'liujinhao0519@163.com',
              ['liujinhao@secrul.cn'], fail_silently=False)
    return redirect(reverse('salary_lists'))
