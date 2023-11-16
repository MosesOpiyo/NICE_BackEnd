from rest_framework import serializers
from .models import CoffeeProducts,Ratings,ProcessedProducts,FarmerProfile
from Authentication.models import Account
from Authentication.serializers import UserSerializer
from datetime import datetime

class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoffeeProducts
        fields = '__all__'
    def save(self,request):
        farmer = Account.objects.get(email=self.validated_data['email'])
        product = CoffeeProducts(name=self.validated_data['name'],
                                 quantity=self.validated_data['quantity'],
                                 date=datetime.now(),
                                 warehouse_approved=False,
                                 producer = farmer,
                                 email=self.validated_data['email'],
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
    producer = UserSerializer(read_only=True)
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
    
class ProfileSerializers(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True)
    class Meta:
        model = FarmerProfile
        fields = '__all__'

    def save(self,request):
        profile = FarmerProfile(
            farmer = request.user,
            county = self.validated_data['county'],
            wet_mill_name = self.validated_data['wet_mill_name'],
            society_name = self.validated_data['society_name'],
            factory_manager = self.validated_data['factory_manager'],
            no_of_farmers = self.validated_data['no_of_farmers'],
            total_acreage = self.validated_data['total_acreage'],
            no_of_trees = self.validated_data['no_of_trees'],
            altitude = self.validated_data['altitude'],
            harvest_season = self.validated_data['harvest_season'],
            annual_rainfall_amount = self.validated_data['annual_rainfall_amount'],
            coffee_variety = self.validated_data['coffee_variety'],
            certification_type = self.validated_data['certification_type'],
            availability = self.validated_data['availability'],
            location = self.validated_data['location'],
            farm_area = self.validated_data['farm_area']
        )
        profile.save()
        return profile
    
class UpdateProfileSerializers(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True)
    class Meta:
        model = FarmerProfile
        fields = '__all__'

    def save(self,id,request):
        farmer_profile = FarmerProfile.objects.get(id=id)
        farmer_profile.county = self.validated_data['county'],
        farmer_profile.wet_mill_name = self.validated_data['wet_mill_name'],
        farmer_profile.society_name = self.validated_data['society_name'],
        farmer_profile.factory_manager = self.validated_data['factory_manager'],
        farmer_profile.no_of_farmers = self.validated_data['no_of_farmers'],
        farmer_profile.total_acreage = self.validated_data['total_acreage'],
        farmer_profile.no_of_trees = self.validated_data['no_of_trees'],
        farmer_profile.altitude = self.validated_data['altitude'],
        farmer_profile.harvest_season = self.validated_data['harvest_season'],
        farmer_profile.annual_rainfall_amount = self.validated_data['annual_rainfall_amount'],
        farmer_profile.coffee_variety = self.validated_data['coffee_variety'],
        farmer_profile.certification_type = self.validated_data['certification_type'],
        farmer_profile.availability = self.validated_data['availability'],
        farmer_profile.location = self.validated_data['location'],
        farmer_profile.farm_area = self.validated_data['farm_area']
        farmer_profile.save()
        return farmer_profile
    
class GetProfileSerializers(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True)
    class Meta:
        model = FarmerProfile
        fields = "__all__"
    
class GetRatingSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Ratings
        fields = '__all__'

class ProcessedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedProducts
        fields = ['img','price','quantity']

    def save(self):
        product = ProcessedProducts(
            img=self.validated_data['img'],
            price=self.validated_data['price'],
            quantity=self.validated_data['quantity']
        )
        product.save()
        return product

    
class GetProcessedProductsSerializers(serializers.ModelSerializer):
    product = GetProductsSerializers(read_only=True)
    rating = GetRatingSerializers(read_only=True,many=True)

    class Meta:
        model = ProcessedProducts
        fields = '__all__'
    






        

