from django.urls import path
from Warehouser import views as warehouse

urlpatterns = [
    path("Warehouse",warehouse.WarehouseClass.get_warehouse,name="warehouse"),
    path("Products",warehouse.WarehouseClass.get_warehouse_products,name="products"),
]