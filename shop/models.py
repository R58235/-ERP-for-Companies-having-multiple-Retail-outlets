import datetime
from pyexpat import model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class Shop(models.Model):
    shop_code= models.CharField(max_length=3)
    name= models.CharField(max_length=15)
    address= models.CharField(max_length=100)
    city= models.CharField(max_length=15)
    state= models.CharField(max_length=15)
    website= models.CharField(max_length=40, default="website")
    email= models.CharField(max_length=50,default="email")
    phone_no1= models.CharField(max_length=10)
    phone_no2= models.CharField(max_length=10)
    GST_no= models.CharField(max_length=15)
    shop_current_invoice_no= models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.name
    
class Account(models.Model):
    phone_no= models.CharField(max_length=10)
    name= models.CharField(max_length=20)
    address= models.CharField(max_length=50)
    city= models.CharField(max_length=15)
    state= models.CharField(max_length=15)
    def __str__(self) -> str:
        return self.name
    
class PaymentMethod(models.Model):
    paymentMethod= models.CharField(max_length=10)
    balance= models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.paymentMethod
    
class FinanceCompany(models.Model):
    name= models.CharField(max_length=20)
    
    
class Invoice(models.Model):
    shop= models.ForeignKey(Shop, on_delete=models.CASCADE)
    account= models.ForeignKey(Account, on_delete=models.CASCADE)
    finance= models.ForeignKey(FinanceCompany, on_delete=models.CASCADE)
    date_time_created= models.DateTimeField(auto_now_add=True)
    invoice_no= models.IntegerField(default=0)
    cancelled= models.CharField(max_length=3,default="NO")
    total_amount= models.IntegerField(default=0)
    total_qty=models.IntegerField(default=0)
    taxable_amount= models.IntegerField(default=0)
    due= models.IntegerField(default=0)
    cgst= models.IntegerField(default=0)
    sgst= models.IntegerField(default=0)
    igst= models.IntegerField(default=0)
    remark= models.CharField(max_length=100)
    emi= models.IntegerField(default=0)
    downpayment= models.IntegerField(default=0)
    financeDisbursement= models.IntegerField(default=0)
    
    def is_cancelled(self):
        if self.cancelled=="NO":
            return False
        else:
            return True
    def __str__(self) -> str:
        return self.shop.shop_code+"/"+self.invoice_no
    
class Payment(models.Model):
    invoice= models.ForeignKey(Invoice, on_delete=models.CASCADE)
    paymentMethod= models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount= models.IntegerField(default=0)
    date_time_created= models.DateTimeField(auto_now_add=True)
    
class Hsn(models.Model):
    code= models.CharField(max_length=8)
    description= models.CharField(max_length=20)
    rate= models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.code
    
class Product(models.Model):
    invoice= models.ForeignKey(Invoice, on_delete=models.CASCADE)
    hsn= models.ForeignKey(Hsn, on_delete=models.CASCADE)
    name= models.CharField(max_length=50)
    description= models.CharField(max_length=100,default="")
    qty= models.IntegerField(default=0)
    price= models.IntegerField(default=0)
    taxable_value= models.IntegerField(default=0)
    cgst= models.IntegerField(default=0)
    sgst= models.IntegerField(default=0)
    igst= models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.name
