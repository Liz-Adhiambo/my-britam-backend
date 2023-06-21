from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


def generate_ref_code():
    code=str(uuid.uuid4()).replace('-', '').replace[:12]
    return code
    

# Create your models here.
class User(AbstractUser):
    is_user = models.BooleanField('user status', default=False)
    is_insurer= models.BooleanField('insurer status', default=False)
    first_login= models.BooleanField(default=True)

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,blank=True)
    middle_name = models.CharField(max_length=255,blank=True, null=True)
    dob = models.CharField(max_length=50,blank=True, null=True)
    code=models.CharField(max_length=50,blank=True, null=True)
    referred_by=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True, null=True, related_name='referred_by')
    referral_link=models.CharField(max_length=450,blank=True, null=True)
    gender = models.CharField(max_length=50,blank=True, null=True)
    phone_number = models.CharField(max_length=255,blank=True, null=True)
    full_name=models.CharField(max_length=455, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.code == None:
            code=str(uuid.uuid4()).replace('-', '')[:12]
            self.code = code
            self.full_name = self.user.first_name + ' ' + self.middle_name + ' ' + self.user.last_name
        self.referral_link=f'https://my-britam-backend-production.up.railway.app/api/v1/signup/'+(self.code)
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

class PolicyTypes(models.Model):
    name = models.CharField(blank=True, null=True)
    p_type = models.CharField(max_length=255,blank=True, null=True)
    description = models.CharField(max_length=255,blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

class Policy(models.Model):
    policy_type =models.ForeignKey(PolicyTypes, on_delete=models.CASCADE, blank=True, null=True)
    policy_name = models.CharField(max_length=255,blank=True, null=True)
    policy_duration = models.CharField(max_length=50,blank=True, null=True)
    policy_status= models.CharField(max_length=50,blank=True, null=True)
    policy_details=models.TextField(blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.policy_name

class UserPolicy(models.Model):
    Policy_number =models.CharField(max_length=250,blank=True, null=True)
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE, blank=True, null=True)
    is_draft=models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    frequency= models.CharField(max_length=250,blank=True, null=True)
    premium=models.CharField(max_length=250,blank=True, null=True)
    next_premium=models.CharField(max_length=250,blank=True, null=True)
    full_name=models.CharField(max_length=250,blank=True,null=True)
    dob=models.CharField(max_length=250,blank=True, null=True)
    postal_address=models.CharField(max_length=250,blank=True, null=True)
    telephone_number=models.CharField(max_length=250,blank=True, null=True)
    email=models.CharField(max_length=250,blank=True, null=True)
    pin=models.CharField(max_length=250,blank=True, null=True)
    life_assured=models.CharField(max_length=250,blank=True, null=True)
    country=models.CharField(blank=True, null=True)
    nationality=models.CharField(blank=True, null=True)
    marital_status=models.CharField(blank=True, null=True)
    resident_country=models.CharField(blank=True, null=True)
    sum_assured=models.CharField(blank=True, null=True)
    status=models.CharField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    # def __str__(self):
    #     return self.status
    
    

