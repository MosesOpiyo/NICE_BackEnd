from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CoffeeProducts
from .serializers import ProductsSerializers


# Create your views here.
class Farming:
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def newProduct(request):
        data = {}
        serializers = ProductsSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save(request)
            data = "New Product Created"
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializers.error_messages
            Response(data,status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def getProducts(request):
        data = {}
        products = CoffeeProducts.objects.select_related('producer').filter(producer=request.user)
        data =  ProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)