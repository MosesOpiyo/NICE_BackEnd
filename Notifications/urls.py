from django.urls import path
from Notifications import views as Notification

urlpatterns = [
    path("notifications",Notification.Notifications.get_notifications,name="notifications"),
]