from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from .serializers import *

from .models import *

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def user_login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print("one")

    user = authenticate(request, username=username, password=password)
    print("weny")

    if user is not None:
        print("9")
        # Authentication successful
        users=User.objects.get(username=username)
        refresh = RefreshToken.for_user(user)

        # Return the user's details, refresh token, and access token in the response
        return Response({
            'Success': True,
            'Code': 200,
            'Details': {
                'email': users.email,
                'first_name': users.first_name,
                'last_name': users.last_name,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=HTTP_200_OK)
    else:
        # Authentication failed
        return Response({
            'Success': False,
            'Code': 401,
            'message': 'Invalid email or password.'
        }, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def User_signup_view(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        User = get_user_model()
        user = User.objects.create_user(
            email=request.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],

            is_driver=True,
        )

        driver = serializer.save(user=user)

        return Response({'Success': True, 'Code': 200, 'message': 'Driver created successfully.'}, status=HTTP_201_CREATED)
    else:
        return Response({'Success': False, 'Code': 400, 'message': serializer.errors}, status=HTTP_400_BAD_REQUEST)

