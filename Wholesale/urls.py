from django.urls import path
from views import Wholesale as views

urlpatterns = [
    path('/Wholesale',views.new_whole_enterprise,name='new_wholesaler')
]