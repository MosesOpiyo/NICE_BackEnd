from django.urls import path
from Warehouser import views as warehouse

urlpatterns = [
    path("Warehouse",warehouse.WarehouseClass.get_warehouse,name="warehouse"),
    path("Products",warehouse.WarehouseClass.get_warehouse_products,name="products"),
    path("Shipping/<int:id>",warehouse.shippingClass.shipToWarehouser,name="shipping"),
    path("Manifests",warehouse.shippingClass.getManifests,name="manifests"),
]