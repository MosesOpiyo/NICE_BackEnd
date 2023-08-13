from django.urls import path
from Depending_Accounts import views as views

urlpatterns = [
    path("FarmerRegistration",views.Depending.farmer_registration_view,name="new_farmer"),
]