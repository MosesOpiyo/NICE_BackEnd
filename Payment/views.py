from decouple import config
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status as Status

import requests
import json
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
        "mode": "live", # sandbox or live
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
            print("Payment created successfully")

            for link in payment.links:
                if link.rel == "approval_url":
                    # Convert to str to avoid Google App Engine Unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                    approval_url = str(link.href)
                    print("Redirect for approval: %s" % (approval_url))
                    return Response(data=approval_url,status=Status.HTTP_200_OK)               
        else:
            print(payment.error)