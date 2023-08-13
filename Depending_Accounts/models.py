from django.db import models

# Create your models here.
class Depending_Account(models.Model):
    username = models.TextField(default="")
    email = models.EmailField(verbose_name="email",max_length=100,unique=True,null=True)
    password = models.TextField(default="")

    def __str__(self):
        return self.username

    