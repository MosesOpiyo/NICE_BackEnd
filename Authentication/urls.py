from django.urls import path
from Authentication import views as views

urlpatterns = [
    path("AdminRegistration",views.admin_registration_view,name="new_admin"),
    path("FarmerRegistration",views.farmer_registration_view,name="new_farmer"),
    path("WarehouserRegistration",views.warehouser_registration_view,name="new_warehouser"),
    path("OriginWarehouserRegistration",views.origin_warehouser_registration_view,name="origin_warehouser"),
    path("Registration",views.registration_view,name="buyer"),
    path("Login",views.login,name='login'),
    path("Verification",views.Verification,name='verify'),
    path("Profile",views.get_profile,name='profile'),
    path("ProfilePicture",views.profilePicture,name='picture'),
]