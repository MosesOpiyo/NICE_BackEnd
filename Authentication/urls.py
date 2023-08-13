from django.urls import path
from Authentication import views as views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views as special_views

urlpatterns = [
    path("AdminRegistration",views.admin_registration_view,name="new_admin"),
    path("FarmerRegistration",views.farmer_registration_view,name="new_farmer"),
    path("WarehouserRegistration",views.warehouser_registration_view,name="new_warehouser"),
    path("Registration",views.registration_view,name="buyer"),
    path("Login",special_views.obtain_auth_token),
    path("Profile",views.get_profile,name='profile')
]