from decouple import config
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status as Status


import time
from Authentication.models import Account
from Orders.models import Order,Cart
from Orders.serializers import OrderSerializers
from .models import Receipt
from .serializers import AddressSerializers,ReceiptSerializers,SubscriptionSerializer
from decouple import config
from .utils import make_paypal_payment,verify_paypal_payment
            
class ProcessingPayment:
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def newPayment(request):
        address_serializer = AddressSerializers(data=request.data)
        new_receipt = ReceiptSerializers(data=request.data)
        buyer = Account.objects.get(id=request.user.id)
        cart = Cart.objects.get(buyer = buyer)
        if address_serializer.is_valid():
            address = address_serializer.save()
            if new_receipt.is_valid():
                receipt = new_receipt.save()
                receipt.address_info = address
                receipt.buyer = buyer
                new_order = Order.objects.create(
                    buyer = buyer
                )
                for item in cart.products.all():
                    new_order.product.add(item)
                new_order.save()
                receipt.order = new_order

        status,payment_id,approved_url = make_paypal_payment(receipt)
        receipt.payment_id = payment_id
        receipt.save()
        if status:
            return Response(data={"success":True,"msg":"payment link has been successfully created","approved_url":approved_url,"receipt_id":receipt.id},status=201)
        else:
            return Response(data={"success":False,"msg":"Authentication or payment failed"},status=Status.HTTP_400_BAD_REQUEST)

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def verifyPayment(request,id):
        PAYMENT_PERIOD = 300
        MAX_ATTEMPTS = 20
        DELAY_SECONDS = 120
        
        time.sleep(PAYMENT_PERIOD)
        try:
            receipt = Receipt.objects.get(id=id)
        except receipt.DoesNotExist:
            return Response({"success": False, "msg": "Receipt not found"}, status=Status.HTTP_404_NOT_FOUND)
        
        attempts = 0
        payment_status = False
        while attempts < MAX_ATTEMPTS:
            payment_status = verify_paypal_payment(payment_id=receipt.payment_id)
            if payment_status:
                receipt.paid = receipt.order.is_paid = True
                OrderSerializers.create_order(user=request.user)
                return Response(data="payment successful", status=Status.HTTP_202_ACCEPTED)
            else:
                attempts += 1
                print(f"Payment not Found")
                time.sleep(DELAY_SECONDS)  # Delay before the next attempt
        receipt.delete()
        return Response({"success": False, "msg": "payment failed or cancelled after multiple attempts"}, status=Status.HTTP_400_BAD_REQUEST)
        
