from django.db import models
from datetime import datetime

class Notification(models.Model):
    message = models.TextField(blank=True)
    seen = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=datetime(2023, 1, 1, 12, 0, 0))
    route = models.TextField(blank=True)

    def __str__(self):
        return self.message

