from django.urls import path
from .views import Payment,PaymentII,getPayments

urlpatterns = [
    path('paypal/create/<path:amount>',PaymentII.create_payment, name='ordercreate'),
    path('paypal/validate/',Payment.validatePayment, name='paypalvalidate'),
    path('Payments',getPayments.get_payments, name='payments'),
]