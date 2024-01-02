from django.urls import path
from Warehouser import views as warehouse

urlpatterns = [
    path("Warehouse",warehouse.WarehouseClass.get_warehouse,name="warehouse"),
    path("EditWarehouse/<str:key>",warehouse.WarehouseClass.updateProfile,name="profile"),
    path("Warehousers",warehouse.shippingClass.getWarehousers,name="warehousers"),
    path("Products",warehouse.WarehouseClass.get_warehouse_products,name="products"),
    path("Shipping/<int:id>",warehouse.shippingClass.shipToWarehouser,name="shipping"),
    path("Manifests",warehouse.shippingClass.getManifests,name="manifests"),
    path("WarehouseManifest/<int:number>",warehouse.shippedClass.getManifest,name="manifests"),
    path("Manifest/<int:id>",warehouse.shippingClass.createManifest,name="manifest")
]