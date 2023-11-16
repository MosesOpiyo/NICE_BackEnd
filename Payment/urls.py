from django.urls import path
from .views import Payment,PaymentII

urlpatterns = [
    path('paypal/create/<int:amount>', PaymentII.create_payment, name='ordercreate'),
    path('paypal/validate/', Payment.validatePayment, name='paypalvalidate'),
]