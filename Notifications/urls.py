from django.urls import path
from Notifications import views as Notification

urlpatterns = [
    path("notifications",Notification.Notifications.getNotifications,name="notifications"),
]