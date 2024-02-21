from decouple import config
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status as Status

import requests
import json
from django.utils import timezone
from Farming.models import ProcessedProducts
from Authentication.models import Account
from Warehouser.models import Warehouse
from Orders.models import Order,Cart
from .models import Payments
from .serializers import PaymentSerializers
from decouple import config
from .utils import make_paypal_payment,verify_paypal_payment

class Payment:
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def createPayment(self,amount):
        data = {}
        amount=amount
        status,payment_id,approved_url=make_paypal_payment(amount=amount,currency="USD",return_url="https://nicedirectcoffee.com/payment/paypal/success/",cancel_url="https://nicedirectcoffee.com")
        if status:
            return Response(data={"success":True,"msg":"payment link has been successfully created","approved_url":approved_url},status=201)
        else:
            return Response(data={"success":False,"msg":"Authentication or payment failed"},status=Status.HTTP_202_ACCEPTED)
    
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def validatePayment(self, request, *args, **kwargs):
        data = {}
        payment_id=request.data.get("payment_id")
        payment_status=verify_paypal_payment(payment_id=payment_id)
        if payment_status:  
            return Response(data="payment improved",status=Status.HTTP_202_ACCEPTED)
        else:
            return Response({"success":False,"msg":"payment failed or cancelled"},status=Status.HTTP_400_BAD_REQUEST)
        

import paypalrestsdk
from django.http import HttpResponseRedirect

class PaymentII:
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def create_payment(request,amount):
        rounded_amount = round(float(amount),2)
        paypalrestsdk.configure({
        "mode": "live",
        "client_id": config('PAYPAL_CLIENT_ID'),
        "client_secret": config('PAYPAL_SECRET') })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment/execute",
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "amount": {
                    "total": rounded_amount,
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            cart = Cart.objects.get(buyer=request.user)
            
            if cart.products.count() == 1:
                order = Order.objects.create(
                    buyer = request.user
                )
                for item in cart.products.all():
                    warehouser = Account.objects.get(index=item.code)
                    warehouse = Warehouse.objects.get(warehouser=warehouser)
                    order.product.add(item)
                    order.warehouse = warehouse
                    order.date = timezone.now().date()
                    order.is_fulfilled = False
                    order.save()
            elif cart.products.count() > 1:
                duplicate_codes = []
                for item in cart.products.all():
                    if item not in duplicate_codes:
                        duplicate_codes.append(item)
                for item in duplicate_codes:
                    warehouser = Account.objects.get(index=item.code)
                    warehouse = Warehouse.objects.get(warehouser=warehouser)
                order = Order.objects.create(
                        buyer = request.user,
                        warehouse=warehouse
                    )
                order.product.set(cart.products.all())
            payment = Payments.objects.create(
               order = order,
               amount = amount
            )      
            print("Payment created successfully")
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return Response(data=approval_url,status=Status.HTTP_200_OK)           
        else:
            print(payment.error)
            return Response(data=payment.error,status=Status.HTTP_400_BAD_REQUEST) 
        
class getPayments:
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def get_payments(request):
        data = {}
        farmer_payments = []
        orders = Payments.objects.all()
        for order in orders:
            for product in order.order.product.all():
                if product.product.product.producer == request.user:
                    if order not in farmer_payments:
                        farmer_payments.append(order)
                    else:
                        pass
        data = PaymentSerializers(farmer_payments,many=True).data
        return Response(data,status=Status.HTTP_200_OK)
