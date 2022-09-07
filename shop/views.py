from pickle import NONE
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from shop.forms import shopForm
from .models import FinanceCompany, PaymentMethod, Shop, Account, Invoice, Product, Hsn, Payment
from django.urls import reverse
import csv
from .forms import productForm, shopForm
from .forms import accountForm
from shop.reportlabPdf import invoicePdf

def hello(c):
    c.drawString(100,100,"Hello World")

def index(request):
    shop_list= Shop.objects.all
    
    context = {'shop_list': shop_list}
    return render(request, 'shop/index.html', context)

def createNewShop(request):
    
    if request.method == 'GET':
        form = shopForm()
        return render(request, 'shop/createNewShop.html',{'form':form})
    
    elif request.method == 'POST':
        form= shopForm(request.POST)
        
        if form.is_valid():
            shop_code = form.cleaned_data['shop_code']
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            phoneNo1 = form.cleaned_data['phone_no1']
            phoneNo2 = form.cleaned_data['phone_no2']
            email= form.cleaned_data['email']
            website= form.cleaned_data['website']
            gst_no = form.cleaned_data['GST_no']
            current_invoice_no = 0
            try:
                s=Shop.objects.get(shop_code=shop_code)
            except (KeyError, Shop.DoesNotExist):
                shop_list= Shop.objects.all()
                shop = Shop(shop_code=shop_code,name=name,address=address,city=city,state=state,phone_no1=phoneNo1,phone_no2=phoneNo2,email=email,website=website,GST_no=gst_no,shop_current_invoice_no=current_invoice_no)
                shop.save()
                return render(request, 'shop/index.html',{'shop_list':shop_list,'message': "Shop Added Successfully"})
            else:
                return render(request, 'shop/createNewShop.html',{'form':form,'message': "Shop with Similar Shop Code exists create New!"})

def createNewAccount(request):
    
    if request.method == 'GET':
        form = accountForm()
        return render(request, 'shop/createNewAccount.html',{'form': form})
    
    elif request.method == 'POST':
        form= accountForm(request.POST)
        
        if form.is_valid():
            
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            phone_no = form.cleaned_data['phone_no']
            try:
                a=Account.objects.get(phone_no=phone_no)
            except(KeyError, Account.DoesNotExist):
                account = Account(phone_no=phone_no,name=name,address=address,city=city,state=state)
                account.save()
                return render(request, 'shop/createNewAccount.html',{'form': form, 'message': "Account Added Successfully"})
            else:
                return render(request, 'shop/createNewAccount.html',{'form': form, 'message': "Account with similar phone No Exists, Please fill form Again"})

def dashboard(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    if request.method=="GET":
        return render(request, 'shop/dashboard.html', {'shop': shop})
    elif request.method=="POST":
        try:
            selected_account = Account.objects.get(phone_no=request.POST['account'])
        except (KeyError, Account.DoesNotExist):
            return render(request, 'shop/dashboard.html' , {'shop': shop,
                'error_message': "The Account does not exist, Please search another or create new",
            })
        else:
            return HttpResponseRedirect(reverse('shop:accountLedger', args=(shop.id,selected_account.id,)))

def salesRegister(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    invoice_list= Invoice.objects.filter(shop=shop)
    return render(request, 'shop/salesRegister.html',{'shop':shop, 'invoice_list':invoice_list})

def accountLedger(request, shop_id,account_id):
    shop = get_object_or_404(Shop,pk=shop_id)
    account = get_object_or_404(Account, pk=account_id)
    invoice_list= Invoice.objects.filter(account=account)
    return render(request, 'shop/accountLedger.html',{'shop':shop,'account':account, 'invoice_list':invoice_list})

def selectAccount(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    
    if request.method == 'GET':
        return render(request, 'shop/selectAccount.html', {'shop': shop})
    
    elif request.method == 'POST':
        try:
            selected_account = Account.objects.get(phone_no=request.POST['account'])
        except (KeyError, Account.DoesNotExist):
            return render(request, 'shop/selectAccount.html' , {'shop': shop,
                'error_message': "The Account does not exist, Please search another or create new",
            })
        else:
            shop.shop_current_invoice_no+=1
            shop.save()
            invoice = Invoice(shop=shop, account=selected_account, finance=FinanceCompany.objects.get(pk=1),invoice_no= shop.shop_current_invoice_no)
            invoice.save()
            return HttpResponseRedirect(reverse('shop:addDetails', args=(shop.id, selected_account.id, invoice.id)))
        
def addDetails(request, shop_id, account_id, invoice_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    account = get_object_or_404(Account, pk=account_id)
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    product_list = invoice.product_set.all()
    payment_list = invoice.payment_set.all()
    finance_list = FinanceCompany.objects.all()
    if request.method == 'GET':
        return render(request, 'shop/addDetails.html', {'shop': shop, 'account':account, 'invoice': invoice,'product_list':product_list,'payment_list':payment_list,'finance_list':finance_list})
    elif request.method == 'POST':
        finance= FinanceCompany.objects.get(pk=request.POST['finance'])
        invoice.finance=finance
        emi= int(request.POST['emi'])
        invoice.emi=emi
        dp= int(request.POST['dp'])
        invoice.downpayment=dp
        disbursement= int(request.POST['disbursement'])
        invoice.financeDisbursement=disbursement
        remark= request.POST['remark']
        invoice.remark= remark
        invoice.due=invoice.due-disbursement
        invoice.save()
        return invoicePdf(invoice)
         
def addProducts(request, shop_id, account_id, invoice_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    account = get_object_or_404(Account, pk=account_id)
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    form= productForm()
    hsn_list= Hsn.objects.all()
    if request.method == 'GET':
        form= productForm()
        return render(request,'shop/addProducts.html',{'shop':shop, 'account':account, 'invoice':invoice, 'hsn_list':hsn_list, 'form':form})
    elif request.method == 'POST':
        form= productForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            qty = form.cleaned_data['qty']
            price = form.cleaned_data['price']
            hsn = Hsn.objects.get(pk=request.POST['hsn'])
            taxable_value= (qty*price)/((100+hsn.rate)/100)
            cgst= (taxable_value*hsn.rate)/200
            sgst= cgst
            igst=0
            product= Product(invoice=invoice, name=name, description=description, qty=qty, price=price, hsn=hsn, taxable_value=taxable_value, cgst=cgst, sgst=sgst, igst=igst)
            product.save()
            invoice.due+=(product.qty * product.price)
            invoice.total_qty+=product.qty
            invoice.total_amount+= product.price * product.qty
            invoice.taxable_amount+= product.taxable_value
            invoice.cgst+= product.cgst
            invoice.sgst+= product.sgst
            invoice.igst+= product.igst
            invoice.save()
            return HttpResponseRedirect(reverse('shop:addDetails', args=(shop.id, account.id, invoice.id)))
    
def addPayment(request, shop_id, account_id, invoice_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    account = get_object_or_404(Account, pk=account_id)
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    paymentMethod_list= PaymentMethod.objects.all()
    if request.method == 'GET':
        return render(request,'shop/addpayment.html',{'invoice':invoice, 'shop':shop, 'account':account,'paymentMethod_list':paymentMethod_list})
    elif request.method == 'POST':
        amount = int(request.POST['amount'])
        paymentMethod = PaymentMethod.objects.get(pk=request.POST['paymentMethod'])
        payment= Payment(invoice=invoice, paymentMethod=paymentMethod, amount=amount,)
        # paymentMethod.balance +=amount
        paymentMethod.save()
        payment.save()
        invoice.due=invoice.due-payment.amount
        invoice.save()
        return HttpResponseRedirect(reverse('shop:addDetails', args=(shop.id, account.id, invoice.id)))
    
def printInvoice(request, invoice_id):
    invoice= get_object_or_404(Invoice, pk=invoice_id)
    return invoicePdf(invoice)
    

def editInvoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice.cancelled="YES"
    invoice.save()
    shop=invoice.shop
    invoice_list= Invoice.objects.filter(shop=shop)
    return render(request, 'shop/salesRegister.html',{'shop':shop,'invoice_list':invoice_list})

def viewInvoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    shop= invoice.shop
    account= invoice.account
    product_list= Product.objects.filter(invoice=invoice)
    payment_list= Payment.objects.filter(invoice=invoice)
    return render(request, 'shop/viewInvoice.html',{'invoice':invoice,'shop':shop,'account':account,'product_list':product_list,'payment_list':payment_list})
    
# def accountExitsOrNot(request):
#     path=request.path
#     try:
#         selected_account = Account.objects.get(phone_no=request.POST['account'])
#     except (KeyError, Account.DoesNotExist):
#         return render(request, path, {
#             'error_message': "The Account does not exist, Please select another or create new",
#         })
#     else:
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('shop:addProduct', args=(selected_account.id)))



