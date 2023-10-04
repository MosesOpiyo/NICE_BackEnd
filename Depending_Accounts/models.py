from django.db import models

# Create your models here.
class Pending_Account(models.Model):
    index = models.CharField(max_length=10,default="")
    username = models.TextField(default="")
    email = models.EmailField(verbose_name="email",max_length=100,unique=True,null=True)
    phone_number = models.CharField(max_length=9,default=0)
    farmer_registration_number = models.IntegerField(default=0)


    def __str__(self):
        return self.username

    