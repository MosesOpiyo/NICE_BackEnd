from django.urls import path
from .views import Admin

urlpatterns = [
    path("AllBuyers",Admin.allBuyers,name="all_buyers"),
    path("AllWarehousers",Admin.allWarehousers,name="all_warehousers"),
    path("AllFarmers",Admin.allFarmers,name="all_farmers"),
    path("ActiveAdmins",Admin.activeAdmins,name="active_admins"),
    path("WarehousingRequests",Admin.warehousingRequests,name="requests"),
    path("ProcessedProducts",Admin. getProcessedProduct,name="products"),
    path("Requests",Admin.getProductRequest,name="requests"),
    path("deleteUser/<int:id>",Admin.deleteUser,name="delete"),
    
]