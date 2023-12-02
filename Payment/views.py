from decouple import config
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status as Status

import requests
import json
from Farming.models import ProcessedProducts
from Authentication.models import Account
from Warehouser.models import Warehouse
from Orders.models import Order,Cart
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
                    "total": amount,
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
                    order.save()
            elif cart.products.count() > 1:
                duplicate_codes = []
                for item in cart.products.all():
                    if cart.products.count(item.code) > 1:
                        duplicate_codes.append(item)
                for item in duplicate_codes:
                    warehouser = Account.objects.get(index=item.code)
                    warehouse = Warehouse.objects.get(warehouser=warehouser)
                    order = Order.objects.get(
                            warehouser=warehouser
                        )
                    if order:
                        if item.code == warehouser.index and order.product.contains(item):
                            pass
                        elif item.code == warehouser.index and ~order.product.contains(item):
                            order.product.add(item) 
                        elif item.code != warehouser.index and ~order.product.contains(item):
                            pass
                    else:
                        order = Order.objects.create(
                           buyer = request.user,
                           warehouser=warehouser
                        )
                        if item.code == warehouser.index and order.product.contains(item):
                            pass
                        elif item.code == warehouser.index and ~order.product.contains(item):
                            order.product.add(item) 
                        elif item.code != warehouser.index and ~order.product.contains(item):
                            pass
                        

                
            print("Payment created successfully")
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return Response(data=approval_url,status=Status.HTTP_200_OK)           
        else:
            print(payment.error)
            return Response(data=payment.error,status=Status.HTTP_400_BAD_REQUEST)  