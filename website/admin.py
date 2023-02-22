from django.contrib import admin
from . models import Customer, payment
from import_export.admin import ImportExportModelAdmin

class Customeradmin(ImportExportModelAdmin, admin.ModelAdmin):
        list_display= [ 'user', 'name', 'dt']
class payadmin(ImportExportModelAdmin, admin.ModelAdmin):
        list_display= ['opd', 'med', 'procedure', 'Customer_info', 'status']
admin.site.register(Customer, Customeradmin)
admin.site.register(payment, payadmin)