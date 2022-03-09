from django.shortcuts import render
from .models import Orders
from .forms import OrderForm, OrderSelectForm
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.mail import send_mail

# err_msg=0
def order_list(request):
    usr = request.user
    globals()['err_msg'] = 0
    if usr.is_authenticated:
        order_lists = Orders.objects.all()
        context = {}
        context['order_lists'] = order_lists
        # print(err_msg)
        # context['err_msg']=err_msg if err_msg else 0
        context['empty_res'] = 0
        context['err_msg'] = 0
        context['user_type']=usr.get_staff_type()
        return render(request, 'order_list.html', context)
    else:
        return redirect(reverse('login'))


def order_modify(request, order_pk):
    usr = request.user
    globals()['err_msg'] = 0
    if usr.is_authenticated:
        order_tem = Orders.objects.get(pk=order_pk)
        # print(usr.pk, order_tem.creator.pk)
        # print(type(usr), type(order_tem.creator))
        if usr.pk != order_tem.creator.pk:
            order_lists = Orders.objects.all()
            context = {}
            context['order_lists'] = order_lists
            context['empty_res'] = 0
            context['err_msg'] = '不可修改其他员工创建的订单'
            return render(request, 'order_list.html', context)
            # print('OK')
            # globals()['err_msg'] = '不可修改其他员工创建的订单'
            # return redirect(reverse('order_list'))
        if request.method == 'POST':
            ordermodifyform = OrderForm(request.POST)
            if ordermodifyform.is_valid():
                print(ordermodifyform.cleaned_data['order_name'])
                # order_tem.order_name = Product.objects.get(product_name=ordermodifyform.cleaned_data['order_name'])
                order_tem.order_name = ordermodifyform.cleaned_data['order_name']
                order_tem.order_client = ordermodifyform.cleaned_data['order_client']
                order_tem.order_number = ordermodifyform.cleaned_data['order_number']
                order_tem.order_price = ordermodifyform.cleaned_data['order_price']
                order_tem.order_total_price = ordermodifyform.cleaned_data['order_total_price']
                order_tem.order_end = ordermodifyform.cleaned_data['order_end']
                order_tem.order_supplement = ordermodifyform.cleaned_data['order_supplement']
                order_tem.save()
                return redirect(reverse('order_list'))
        else:
            ordermodifyform = OrderForm(initial={'order_name':order_tem.order_name, 'order_client':order_tem.order_client,
                                                 'order_number':order_tem.order_number, 'order_price':order_tem.order_price,
                                                 'order_total_price':order_tem.order_total_price,'order_end':order_tem.order_end,
                                                 'order_supplement':order_tem.order_supplement, 'order_poc':order_tem.order_poc,
                                                 'order_bill_addr':order_tem.order_bill_addr}) # , 'order_date':order_tem.order_time
            context = {}
            context['ordermodifyform'] = ordermodifyform
            # print((order_tem.order_time.strftime('%Y-%m-%d')))
            context['order_date']=order_tem.order_time.strftime('%Y-%m-%d')
            context['order_end'] = order_tem.order_end.strftime('%Y-%m-%d')
            return render(request, 'order_modify.html', context)
    else:
        return redirect(reverse('login'))


def order_delete(request, order_pk):
    usr = request.user
    if usr.is_authenticated:
        order_tem = Orders.objects.get(pk=order_pk)
        if usr.pk != order_tem.creator.pk:
            order_lists = Orders.objects.all()
            context = {}
            context['order_lists'] = order_lists
            context['empty_res'] = 0
            context['err_msg'] = '不可删除其他员工创建的订单'
            return render(request, 'order_list.html', context)
        order_tem.delete()
        return redirect(reverse('order_list'))
    else:
        return redirect(reverse('login'))

def order_append(request):
    usr = request.user
    orderappendform = OrderForm()
    if usr.is_authenticated:
        if usr.get_staff_type()!='委托员工' and usr.get_staff_type()!='管理员':
            return redirect(reverse('order_list'))
        if request.method == 'POST':
            orderappendform = OrderForm(request.POST)
            print(orderappendform.is_valid())
            if orderappendform.is_valid():
                print('Okk')
                order_name = orderappendform.cleaned_data['order_name']
                # order_tem = Product.objects.get(product_name=order_name)
                order_client = orderappendform.cleaned_data['order_client']
                order_number = orderappendform.cleaned_data['order_number']
                order_price = orderappendform.cleaned_data['order_price']
                order_total_price = orderappendform.cleaned_data['order_total_price']
                order_end = orderappendform.cleaned_data['order_end']
                order_supplement = orderappendform.cleaned_data['order_supplement']
                if not order_supplement:
                    order_supplement='无'
                order_poc = orderappendform.cleaned_data['order_poc']
                order_bill_addr = orderappendform.cleaned_data['order_bill_addr']
                order_date = orderappendform.cleaned_data['order_date']
                add = Orders(creator=usr, order_name=order_name, order_client=order_client, order_number=order_number,order_price=order_price,
                             order_total_price=order_total_price, order_end=order_end, order_supplement=order_supplement, order_poc=order_poc,
                             order_bill_addr=order_bill_addr, order_time=order_date)
                add.save()
                # send_mail('Subject here', '有一个新的订单.', 'liujinhao0519@163.com', ['liujinhao@secrul.cn'], fail_silently=False)
                return redirect(reverse('order_list'))
            else:

                context = {}
                context['orderappendform'] = orderappendform
                return render(request, 'order_append.html', context)
        else:
            context = {}
            context['orderappendform'] = OrderForm()
            return render(request, 'order_append.html', context)
    else:
        return redirect(reverse('login'))


def order_select(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            OrderSelectForms = OrderSelectForm(request.POST)
            if OrderSelectForms.is_valid():
                keyword = OrderSelectForms.cleaned_data['keyword']
                valueword = OrderSelectForms.cleaned_data['valueword']
                ans_tem = []
                print(keyword, valueword)
                if keyword == '0':
                    ans_tem=Orders.objects.filter(id=valueword)
                if keyword == '1':  # 产品
                    # ans_tem1 = Product.objects.filter(product_name__contains=valueword)
                    # ans_tem = Orders.objects.filter(order_name__in=ans_tem1)
                    pass
                if keyword == '2':  # 客户
                    ans_tem = Orders.objects.filter(order_client__contains=valueword)

                context = {}
                context['order_lists'] = ans_tem
                context['empty_res'] = 1 if len(ans_tem)==0 else 0
                return render(request, 'order_list.html', context)
        else:
            OrderSelectForms = OrderSelectForm()
            context = {}
            context['OrderSelectForms'] = OrderSelectForms
            return render(request, 'order_select.html', context)
    else:
        return redirect(reverse('login'))
