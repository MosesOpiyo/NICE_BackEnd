from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from cloudinary.models import CloudinaryField
from decouple import config
from Notifications.models import Notification

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have and email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        user.type = Account.Type.ADMIN
        return user

class Account(AbstractBaseUser,PermissionsMixin):
    class Type(models.TextChoices):
        ADMIN = "ADMIN","Admin"
        FARMER = "FARMER","Farmer"
        ORIGINWAREHOUSER = "ORIGINWAREHOUSER","OriginWarehouser"
        WAREHOUSER = "WAREHOUSER","Warehouser"
        BUYER = "BUYER","Buyer"
    index = models.CharField(max_length=10,default="")
    type = models.CharField(_("Type"),max_length=100,choices=Type.choices,default=Type.BUYER)
    email = models.EmailField(verbose_name="email",max_length=100,unique=True,null=True)
    username = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_confirmed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    notifications = models.ManyToManyField(Notification)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

    def delete_user(self):
        self.delete()

class AdminManager(models.Manager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have and email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.set_password(password)
        user.type = Account.Type.ADMIN
        user.save(using=self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = Account.Type.ADMIN)
        return queryset

class Admin (Account):
    proxy=True
    objects = AdminManager()

    def save(self , *args , **kwargs):
        self.type = Account.Type.ADMIN
        return super().save(*args , **kwargs)

class FarmerManager(models.Manager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have and email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.set_password(password)
        user.type = Account.Type.FARMER
        user.save(using=self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = Account.Type.FARMER)
        return queryset

class Farmer(Account):
    proxy=True
    objects = FarmerManager()

    def save(self , *args , **kwargs):
        self.type = Account.Type.FARMER
        return super().save(*args , **kwargs)
    
class OriginWarehouserManager(models.Manager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have and email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.set_password(password)
        user.type = Account.Type.ORIGINWAREHOUSER
        user.save(using=self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = Account.Type.ORIGINWAREHOUSER)
        return queryset

class OriginWarehouser(Account):
    proxy=True
    objects = OriginWarehouserManager()

    def save(self , *args , **kwargs):
        self.type = Account.Type.ORIGINWAREHOUSER
        return super().save(*args , **kwargs)
    
class WarehouserManager(models.Manager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have and email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.set_password(password)
        user.type = Account.Type.WAREHOUSER
        user.save(using=self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = Account.Type.WAREHOUSER)
        return queryset

class Warehouser(Account):
    proxy=True
    objects = WarehouserManager()

    def save(self , *args , **kwargs):
        self.type = Account.Type.WAREHOUSER
        return super().save(*args , **kwargs)
    
class BuyerManager(models.Manager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have and email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.set_password(password)
        user.type = Account.Type.BUYER
        user.save(using=self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = Account.Type.BUYER)
        return queryset

class Buyer(Account):
    proxy=True
    objects = BuyerManager()

    def save(self , *args , **kwargs):
        self.type = Account.Type.BUYER
        return super().save(*args , **kwargs)

class Profile(models.Model):
    profile_pic = CloudinaryField(
        'images',
        default=config('CLD_URL')
    )
    user = models.OneToOneField(
        Account,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    def __str__(self):
        return  f"{self.user}'s profile"

    @receiver(post_save, sender=Token)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=Token)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class VerificationCode(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    code = models.CharField(max_length=5,default=0)