from django.shortcuts import render, redirect
from . import models
from .models import Customer, payment
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from datetime import datetime
from django.contrib import messages
from . serializer import JobReportSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
import xlwt
from datetime import datetime, timezone


def RegisterCustomerAPIView(request):
    return render(request, 'list.html', {"flag": True})


def webview(request):
    pt = payment.objects.all().order_by('-date')
    return render(request, 'users.html', {"pt": pt})


def detail_report(request):
    if request.method == "POST":
        number = request.POST.get("number")
        user = User.objects.filter(username=number).last()
        if "submit1" in request.POST:
            name = request.POST.get('name')
            # phone =request.POST.get('phone')
            opd = request.POST['opd']
            med = request.POST['med']
            procedure = request.POST['procedure']
            # total = request.GET.get(total)
            total = int(opd) + int(med) + int(procedure)
            obj = Customer.objects.filter(user=request.user).last()
            if not obj:
                obj = Customer(name=name,  user=request.user)
                obj.save()
            obj1 = payment(opd=opd, med=med, procedure=procedure,
                           Customer_info=obj, status="yes", total=total)
            obj1.save()
            obj1.refresh_from_db()
            return redirect('paymentHistory')
        if user:
            login(request, user)
            customer = Customer.objects.filter(user=user).last()
            if not customer:
                return render(request, 'list.html')
            paymenthistory = payment.objects.filter(Customer_info=customer)
            return render(request, 'user.html', {"payment": paymenthistory})
        else:
            user1 = User.objects.create_user(
                username=number, password=number[:3]+"@123")
            login(request, user1)
            return render(request, 'list.html')
    return render(request, 'home.html')


def paymentHistory(request):
    obj = Customer.objects.filter(user=request.user).last()
    paymenthistory = payment.objects.filter(
        Customer_info=obj).order_by('-date')
    return render(request, 'user.html', {"payment": paymenthistory})


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('detail')
            else:
                message = 'Login failed!'
    return render(
        request, 'login.html', context={'form': form, 'message': message})


def loginview(request):
    return render(request, 'loggin.html')
# Import the python xlwt module.


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="payment.xls"'

    now = datetime.now(timezone.utc)

    wb = xlwt.Workbook(encoding='utf-8')
    # this will make a sheet named Users Data
    ws = wb.add_sheet('payment Data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Phone no.', 'Name', 'OPD CHARGES',
               'MEDICAL CHARGES', 'PROCEDURE ', 'Total', 'Date']

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = payment.objects.all().values_list('Customer_info__user__username',
                                             'Customer_info__name', 'opd', 'med', 'procedure', 'total')
    row1 = payment.objects.all()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    for i in row1:

        ws.write(row_num, 7, i.date, font_style)

    wb.save(response)

    return response


def download_excel_data(request):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename="1.xls"'

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 1

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['Phone no.', 'Name', 'Opd  Charges',
               'Medicine Charges', 'Procedure ', 'Total', 'Date']

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # get your data, from database or from a text file...
    data = payment.objects.all()  # dummy method to fetch data.
    # data = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in data ]
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.Customer_info.user.username, font_style)
        ws.write(row_num, 1, my_row.Customer_info.name, font_style)
        ws.write(row_num, 2, my_row.opd, font_style)
        ws.write(row_num, 3, my_row.med, font_style)
        ws.write(row_num, 4, my_row.procedure, font_style)
        ws.write(row_num, 5, my_row.total, font_style)
        ws.write(row_num, 6, str(my_row.date.date()), font_style)

    wb.save(response)
    return response