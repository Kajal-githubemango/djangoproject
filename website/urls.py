from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
     path('form', views.RegisterCustomerAPIView, name='register'),
    path('user', views.webview, name='userlist' ),
    path('paymenthistory', views.paymentHistory, name='paymentHistory' ),
    path('home', views.detail_report, name='detail' ),
    path('', views.loginview, name='checkuser' ),
    path('login', views.login_page, name='login' ),
    path('excelsheet', views.download_excel_data, name='export-excel' ),
 
    
    
      
      
    
]