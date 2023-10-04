from django.urls import path
from .views import Admin

urlpatterns = [
    path("AllBuyers",Admin.allBuyers,name="all_buyers"),
    path("AllWarehousers",Admin.allWarehousers,name="all_warehousers"),
    path("AllFarmers",Admin.allFarmers,name="all_farmers"),
    path("PendingAccounts",Admin.allPendingAccounts,name="pending_accounts"),
    path("PendingActivation/<int:id>",Admin.validatePendingAccount,name="activation"),
    path("ActiveAdmins",Admin.activeAdmins,name="active_admins"),
    path("WarehousingRequests",Admin.warehousingRequests,name="requests")
]