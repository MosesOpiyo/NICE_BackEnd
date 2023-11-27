from django.db import models

class Notification(models.Model):
    message = models.TextField(blank=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.message

