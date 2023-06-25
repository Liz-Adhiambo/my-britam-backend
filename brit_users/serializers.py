from .models import *
from rest_framework import serializers, fields

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        if data['email'] == '':
            raise serializers.ValidationError('Email Field Empty')
        if data['password'] == '':
            raise serializers.ValidationError('Password Field Empty')

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','date_joined',)



class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('__all__')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')

class PolicyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyTypes
        fields = ('__all__')

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('__all__')


class UserPolicySerializer(serializers.ModelSerializer):
    policy_id=PolicySerializer
    class Meta:
        model = UserPolicy()
        fields = ('Policy_number','is_draft','policy_id','user','frequency','premium','next_premium','full_name','dob','postal_address','telephone_number','email','pin','life_assured','country','nationality','marital_status','resident_country','sum_assured','status','createdAt','updatedAt')


class User2PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPolicy
        fields = ('__all__')

class ReferredUserSerializer(serializers.ModelSerializer):
    user = UserSerializer2()
    class Meta:
        model = Users
        fields = ['user', 'middle_name', 'dob', 'code', 'referred_by', 'referral_link', 'gender', 'phone_number', 'full_name','bio','profile_photo']
