from django.db import models
from Orders.models import Order

# Create your models here.
class Payments(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,null=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Payment: {self.id}"
    