from django.urls import path
from .views import Pricing as views

urlpatterns = [
    path("New-Price/<int:id>",views.new_price,name="new_price")
]