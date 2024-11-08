from django.urls import path
from .views import Wholesale as views

urlpatterns = [
    path('New-Wholesaler',views.new_whole_enterprise,name='new_wholesaler'),
    path('Established-Wholesaler',views.established_whole_enterprise,name='established_wholesaler')
]