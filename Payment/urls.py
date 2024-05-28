from django.urls import path
from .views import ProcessingPayment

urlpatterns = [
    path('MakePayment',ProcessingPayment.newPayment,name='new-payment'),
    path('VerifyPayment/<int:id>',ProcessingPayment.verifyPayment,name='verify-payment')
]