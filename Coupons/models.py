from django.db import models

# Create your models here.
class Coupon(models.Model):
    name = models.TextField(default='')
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.name