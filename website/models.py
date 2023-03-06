from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

STATUS_CHOICES = (
	('yes', 'Yes'),
	('no', 'No'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null =True, blank=True)
    name = models.CharField( max_length=50)
    # phone =  models.BigIntegerField()
    dt = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return self.name


class payment(models.Model):
    opd = models.IntegerField( null =True, blank= True)
    med = models.IntegerField(null =True, blank= True)
    procedure = models.IntegerField( null =True, blank= True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='no')
    Customer_info = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    total = models.IntegerField(null =True, blank= True)
    date = models.DateTimeField(default=timezone.now)
    # date = models.DateField(default=timezone.now)
    
    
    def __str__(self):
        return self.Customer_info.name