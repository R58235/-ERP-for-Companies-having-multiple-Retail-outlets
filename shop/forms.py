from doctest import debug_script
from django import forms

class shopForm(forms.Form):
    shop_code= forms.CharField(label='Shop Code', min_length=3,max_length=3)
    name= forms.CharField(label='Name', max_length=15)
    address= forms.CharField(label='Address', max_length=100)
    city= forms.CharField(label='City', max_length=15)
    state= forms.CharField(label='State', max_length=15)
    email= forms.CharField(label='Email',max_length=50)
    website= forms.CharField(label='Website',max_length=40)
    phone_no1= forms.CharField(label='Phone No 1', min_length=10, max_length=10)
    phone_no2= forms.CharField(label='Phone No 2', min_length=10, max_length=10)
    GST_no= forms.CharField(label='GST No', min_length=15, max_length=15)
    
class accountForm(forms.Form):
    name= forms.CharField(label='Name', max_length=15)
    address= forms.CharField(label='Address', max_length=50)
    city= forms.CharField(label='City', max_length=15)
    state= forms.CharField(label='State', max_length=15)
    phone_no= forms.CharField(label='Phone No', min_length=10, max_length=10)
    
class productForm(forms.Form):
    name= forms.CharField(label='name', max_length=50)
    description= forms.CharField(label='description', max_length=100)
    qty= forms.IntegerField(label='qty')
    price= forms.IntegerField(label='price')