from django.db import models

# Create your models here.
class Option(models.Model):
    quantity = models.TextField(default="")
    regular_price = models.FloatField(default=0)
    wholesale_price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.quantity}: {self.regular_price}" 

