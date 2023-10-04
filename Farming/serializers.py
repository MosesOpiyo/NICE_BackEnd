from rest_framework import serializers
from .models import CoffeeProducts,Ratings,ProcessedProducts
from Authentication.serializers import UserSerializer
from datetime import datetime

class ProductsSerializers(serializers.ModelSerializer):
    producer = UserSerializer(read_only=True)
    class Meta:
        model = CoffeeProducts
        fields = '__all__'
    def save(self,request):
        product = CoffeeProducts(name=self.validated_data['name'],
                                 quantity=self.validated_data['quantity'],
                                 date=datetime.now(),
                                 warehouse_approved=False,
                                 producer=request.user,
                                 grade=self.validated_data['grade'],
                                 origin=self.validated_data['origin'],
                                 lot_type=self.validated_data['lot_type'],
                                 cup_score=self.validated_data['cup_score'],
                                 cup_notes=self.validated_data['cup_notes'],
                                 cupped_by=self.validated_data['cupped_by'],
                                 processing=self.validated_data['processing'],
                                 drying=self.validated_data['drying'],
                                 caffeine=self.validated_data['caffeine'],
                                 acidity=self.validated_data['acidity'],
                                 level=self.validated_data['level'],
                                 requested_warehousing=True,
                                 shipment_successful=False
                                 )
        product.save()
        return product
    
class GetProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoffeeProducts
        fields = '__all__'

class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ['rating','comment']

    def save(self,request):
        rating = Ratings(
            rating = self.validated_data['rating'],
            user = request.user,
            comment = self.validated_data['comment']
        )
        rating.save()
        return rating
    
class GetRatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'

class ProcessedProductsSerializer(serializers.ModelSerializer):
    product = GetProductsSerializers(read_only=True)
    rating = GetRatingSerializers(read_only=True,many=True)

    class Meta:
        model = ProcessedProducts
        fields = '__all__'
    
class GetProcessedProductsSerializers(serializers.ModelSerializer):
    product = GetProductsSerializers(read_only=True)
    rating = GetRatingSerializers(read_only=True,many=True)

    class Meta:
        model = ProcessedProducts
        fields = '__all__'
    






        

