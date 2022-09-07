from django.urls import path

from . import views

app_name='shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('createNewShop', views.createNewShop, name='createNewShop'),
    path('createNewAccount', views.createNewAccount, name='createNewAccount'),
    path('<int:shop_id>/dashboard', views.dashboard, name='dashboard'),
    path('<int:shop_id>/salesRegister', views.salesRegister, name='salesRegister'),
    path('<int:shop_id>/selectAccount', views.selectAccount, name='selectAccount'),
    path('<int:shop_id>/<int:account_id>/<int:invoice_id>/addDetails', views.addDetails, name='addDetails'),
    path('<int:shop_id>/<int:account_id>/<int:invoice_id>/addProducts', views.addProducts, name='addProducts'),
    path('<int:shop_id>/<int:account_id>/<int:invoice_id>/addPayment', views.addPayment, name='addPayment'),
    path('<int:invoice_id>/editInvoice', views.editInvoice, name='editInvoice'),
    path('<int:invoice_id>/viewInvoice', views.viewInvoice, name='viewInvoice'),
    path('<int:invoice_id>/printInvoice',views.printInvoice, name='printInvoice'),
    path('<int:shop_id>/<int:account_id>/accountLedger', views.accountLedger, name='accountLedger'),
]