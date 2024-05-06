from django.urls import path
from .views import Payment,PaymentII,getPayments,ProcessingPayment

urlpatterns = [
    path('paypal/create/<path:amount>',PaymentII.create_payment, name='ordercreate'),
    path('paypal/validate/',Payment.validatePayment, name='paypalvalidate'),
    path('Payments',getPayments.get_payments, name='payments'),
    path('MakePayment',ProcessingPayment.newPayment,name='new-payment')
]