from django.urls import path
from Authentication import views as views

urlpatterns = [
    path("AdminRegistration",views.admin_registration_view,name="new_admin"),
    path("FarmerRegistration",views.farmer_registration_view,name="new_farmer"),
    path("WarehouserRegistration",views.warehouser_registration_view,name="new_warehouser"),
    path("OriginWarehouserRegistration",views.origin_warehouser_registration_view,name="origin_warehouser"),
    path("Registration",views.registration_view,name="buyer"),
    path("GoogleSignIn",views.google_signin,name="buyer_sign_in"),
    path("PasswordRecovery",views.recoverPassword,name='password'),
    path("Login",views.login,name='login'),
    path("EditData/<str:key>",views.updateData,name='data'),
    path("ChangePassword",views.updatePassword,name='password'),
    path("Verification",views.Verification,name='verify'),
    path("Profile",views.get_profile,name='profile'),
    path("ProfilePicture",views.profilePicture,name='picture'),
    path("DeleteNotifications",views.delete_notification,name='delete'),
]