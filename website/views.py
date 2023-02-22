from django.shortcuts import render, redirect
from . import models
from .models import Customer, payment
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib import messages
from . serializer import JobReportSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login

def RegisterCustomerAPIView(request):
    return render(request, 'list.html', {"flag": True})

def webview(request):
    pt = payment.objects.all().order_by('-Customer_info__dt')
    if request.method == "GET":
        pmt = request.GET.get('searchname')
        if pmt != None:
            pt = payment.objects.filter(Customer_info__name=pmt)
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
    paymenthistory = payment.objects.filter(Customer_info=obj)
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