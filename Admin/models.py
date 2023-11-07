from django.db import models
from Authentication.models import Account
# Create your models here.
class Requests(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)