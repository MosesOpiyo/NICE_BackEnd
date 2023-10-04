from django.db import models

class Notification(models.Model):
    message = models.TextField(blank=True)
    recepient_index = models.CharField(max_length=10,default="")

