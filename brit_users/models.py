from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_user = models.BooleanField('user status', default=False)
    is_insurer= models.BooleanField('insurer status', default=False)
    first_login= models.BooleanField(default=True)

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,blank=True)
    middle_name = models.CharField(max_length=255,blank=True, null=True)
    dob = models.CharField(max_length=50,blank=True, null=True)
    gender = models.CharField(max_length=50,blank=True, null=True)
    phone_number = models.CharField(max_length=255,blank=True, null=True)
    full_name=models.CharField(max_length=455, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.full_name = self.user.first_name + ' ' + self.middle_name + ' ' + self.user.last_name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.full_name

class Profile(models.Model):
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.CharField(max_length=255,blank=True, null=True)
    status = models.CharField(max_length=50,blank=True, null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='profile')

    def __str__(self):
        return self.user