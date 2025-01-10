import binascii,os
import csv
from io import TextIOWrapper
from rest_framework import serializers
from .models import *
from Authentication.models import Account
from Authentication.serializers import UserSerializer
from django.utils import timezone

from NICE_BACK.image import compress_image
from Notifications.models import Notification
from Authentication.models import Farmer
from PIL import Image
from io import BytesIO

class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoffeeProducts
        fields = '__all__'
    def save(self,request):
        farmer = Account.objects.get(email=self.validated_data['email'])
        profile = FarmerProfile.objects.get(farmer=farmer)
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
                                 species=self.validated_data['species'],
                                 acidity=self.validated_data['acidity'],
                                 level=self.validated_data['level'],
                                 requested_warehousing=True,
                                 shipment_successful=False,
                                 certification=profile.certification_type
                                 )
        product.name = product.name.upper()
        product.save()
        
        notification = Notification.objects.create(
            message = "Your Product has been created and registered.",
            route = 'table'  
        )
        farmer.notifications.add(notification)
        return product
    
class GetProductsSerializers(serializers.ModelSerializer):
    producer = UserSerializer(read_only=True)
    class Meta:
        model = CoffeeProducts
        fields = '__all__'

class GetProductsForShopSerializers(serializers.ModelSerializer):
    producer = UserSerializer(read_only=True)
    class Meta:
        model = CoffeeProducts
        fields = [
            'origin',
            'caffeine',
            'cup_score',
            'cup_notes',
            'date',
            'grade',
            'level',
            'name',
            'price',
            'processing',
            'producer',
            'certification'
        ]

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
    
class ExcelProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = "__all__"
        # fields = ['wet_mill_name',
        #           'society_name',
        #           'factory_chairman',
        #           'factory_manager',
        #           'country',
        #           'county',
        #           'no_of_farmers',
        #           'male_farmers',
        #           'female_farmers',
        #           'total_acreage',
        #           'no_of_trees',
        #           'altitude',
        #           'harvest_season',
        #           'annual_rainfall',
        #           'annual_temp',
        #           'varieties',
        #           'farming_method',
        #           'certification_type',
        #           'cherry_production_2019_to_2020',
        #           'cherry_production_2020_to_2021',
        #           'cherry_production_2021_to_2022',
        #           'soil_type',
        #           'processing_method',
        #           'drying_method',
        #           'cupping_notes',
        #           'availability',
        #           'grower_history'
        #           ]

    def save(self):
        # farmer = Farmer.objects.get(
        #     email = request.user.email,
        # )
        # password = binascii.hexlify(os.urandom(10)).decode('utf-8')
        # farmer.set_password(password)
        profile = FarmerProfile(
            county=self.validated_data['COUNTY'],
            country=self.validated_data['COUNTRY'],
            wet_mill_name=self.validated_data['WETMILL NAME'],
            society_name=self.validated_data['SOCIETY NAME'],
            factory_chairman=self.validated_data['FACTORY CHAIRMAN'],
            factory_manager=self.validated_data['FACTORY MANANGER'],
            no_of_farmers=self.validated_data['NO.OF FARMERS'],
            male_farmers=self.validated_data['MALE FARMERS'],
            female_farmers=self.validated_data['FEMALE FARMERS'],
            total_acreage=self.validated_data['TOTAL ACREAGE'],
            no_of_trees=self.validated_data['NO.OF TREES'],
            altitude=self.validated_data['ALTITUDE'],
            harvest_season=self.validated_data['HARVEST SEASON'],
            annual_rainfall=self.validated_data['ANNUAL RAINFALL AMT'],
            annual_temp=self.validated_data['ANNUAL TEMP AMT'],
            varieties=self.validated_data['COFFEE VARIETIES'],
            farming_method=self.validated_data['FARMING METHOD'],
            certification_type=self.validated_data['CERTIFICATION TYPE'],
            cherry_production_2019_to_2020=self.validated_data['CHERRY CHERRY PRODUCTION 2019-2020'],
            cherry_production_2020_to_2021=self.validated_data['CHERRY CHERRY PRODUCTION 2020-2021'],
            cherry_production_2021_to_2022=self.validated_data['CHERRY PRODUCTION 2021-2022'],
            soil_type=self.validated_data['SOIL TYPE'],
            processing_method=self.validated_data['PROCESSIPROCESSING METHODS'],
            drying_method=self.validated_data['DRYING METHOD'],
            cupping_notes=self.validated_data['CUPPING NOTES'],
            availability=self.validated_data['AVAILABILITY'],
            grower_history=self.validated_data["GROWER'S HISTORY"]
        )
        return profile
    
class ProfileSerializers(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True)
    class Meta:
        model = FarmerProfile
        fields = '__all__'

    def save(self,request):
        farmer = Farmer.objects.get(
            email = request.user.email,
        )
        password = binascii.hexlify(os.urandom(10)).decode('utf-8')
        farmer.set_password(password)
        profile = FarmerProfile(
            farmer = farmer,
            county = self.validated_data['county'],
            country = self.validated_data['country'],
            wet_mill_name = self.validated_data['wet_mill_name'],
            society_name = self.validated_data['society_name'],
            estate_name = self.validated_data['estate_name'],
            factory_chairman = self.validated_data['factory_chairman'],
            factory_manager = self.validated_data['factory_manager'],
            no_of_farmers = self.validated_data['no_of_farmers'],
            men = self.validated_data['men'],
            women = self.validated_data['women'],
            total_acreage = self.validated_data['total_acreage'],
            no_of_trees = self.validated_data['no_of_trees'],
            altitude = self.validated_data['altitude'],
            harvest_season = self.validated_data['harvest_season'],
            annual_rainfall_amount = self.validated_data['annual_rainfall_amount'],
            species = self.validated_data['species'],
            varieties = self.validated_data['varieties'],
            farming_method = self.validated_data['farming_method'],
            processing_method = self.validated_data['processing_method'],
            drying_method = self.validated_data['drying_method'],
            certification_type = self.validated_data['certification_type'],
            soil_type = self.validated_data['soil_type'],
            cupping_notes = self.validated_data['cupping_notes'],
            availability = self.validated_data['availability'],
            grower_history = self.validated_data['grower_history'],
            location = self.validated_data['location'],
            farm_area = self.validated_data['farm_area']
        )
        profile.save()
        return profile
    
class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ['rating','comment']

    def save(self,request,id):
        buyer = Buyer.objects.get(
            id = request.user.id,
        )
        rating = Ratings(
            rating = self.validated_data['rating'],
            comment = self.validated_data['comment']
        )
        rating.user = buyer
        rating.save()
        product = ProcessedProducts.objects.get(
            id = id
        )
        product.rating.add(rating)
        product.save()
        return rating

    
class ExcelSerializers(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True)
    class Meta:
        model = FarmerProfile
        fields = '__all__'

    def save(self,request):
        farmer = Farmer.objects.create(
            email = self.validated_data['email'],
            username = self.validated_data['factory_manager'],
        )
        password = binascii.hexlify(os.urandom(10)).decode('utf-8')
        farmer.set_password(password)
        profile = FarmerProfile(
            farmer = farmer,
            county = self.validated_data['county'],
            country = self.validated_data['country'],
            wet_mill_name = self.validated_data['wet_mill_name'],
            society_name = self.validated_data['society_name'],
            factory_chairman = self.validated_data['factory_chairman'],
            factory_manager = self.validated_data['factory_manager'],
            no_of_farmers = self.validated_data['no_of_farmers'],
            men = self.validated_data['men'],
            women = self.validated_data['women'],
            total_acreage = self.validated_data['total_acreage'],
            no_of_trees = self.validated_data['no_of_trees'],
            altitude = self.validated_data['altitude'],
            harvest_season = self.validated_data['harvest_season'],
            annual_rainfall_amount = self.validated_data['annual_rainfall_amount'],
            coffee_variety = self.validated_data['coffee_variety'],
            farming_method = self.validated_data['farming_method'],
            certification_type = self.validated_data['certification_type'],
            soil_type = self.validated_data['soil_type'],
            processing_method = self.validated_data['processing_method'],
            cupping_notes = self.validated_data['cupping_notes'],
            availability = self.validated_data['availability'],
            grower_history = self.validated_data['grower_history'],
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
        fields = ['img','quantity','code']

    def save(self,request,id):
        product = CoffeeProducts.objects.get(id=id)
        farmer = product.producer
        product = ProcessedProducts(
            img = self.validated_data['img'],
            product=product,
            quantity=self.validated_data['quantity'],
            code=request.user.index
        )
        product.save()
        return product
    
class StoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = ['media','caption']

    def compress_image(image_file):
            img = Image.open(image_file)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
        
            img.thumbnail((800, 800))
            
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            return buffer.getvalue()

    def save(self,request):
        user = Account.objects.get(id = request.user.id)
        story = Stories(
            user = user,
            media = self.validated_data['media'],
            caption = self.validated_data['caption']
        )
        story.date_added = None
        story.date_added = timezone.now()
        story.save()
        user
        return story
    
class GetStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = "__all__"

class GetPricingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class GetProcessedProductsSerializers(serializers.ModelSerializer):
    product = GetProductsForShopSerializers(read_only=True)
    pricing = GetPricingSerializers(read_only=True,many=True)
    rating = GetRatingSerializers(read_only=True,many=True)

    class Meta:
        model = ProcessedProducts
        fields = '__all__'
    






        

