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
    class Meta:
        model = UserPolicy
        fields = ('__all__')


class User2PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPolicy
        fields = ('__all__')

