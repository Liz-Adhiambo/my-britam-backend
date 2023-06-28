import base64
import requests
from django.conf import settings
from django.shortcuts import render
import uuid
import datetime 
# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from .serializers import *

from .models import *
from .mpesa import MpesaService
from django.http import HttpResponse





@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def user_login_view(request):
    print("twenty three")
    username = request.data.get('username')
    password = request.data.get('password')
    print("oneklsl")
    try:

        user = authenticate(request, username=username, password=password)
        print("weny")
        print(user)

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
                    'id':users.id,
                    'first_name': users.first_name,
                    'last_name': users.last_name,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=HTTP_200_OK)
    except:
        print('the hell is going on')
    else:
        # Authentication failed
        return Response({
            'Success': False,
            'Code': 401,
            'message': 'Invalid email or password.'
        }, status=HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([])
def User_signup_referral_view(request,code):
    serializer = UsersSerializer(data=request.data)
    try:
        r_code=Users.objects.get(code=code)
        print(r_code.user)
    except:
        return Response({'Success': False, 'Code': 400, 'message': 'That refferral code does not exist.'}, status=HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        email = request.data['email']


        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return Response({'Success': False, 'Code': 400, 'message': 'Email already exists.'}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            username=request.data['username'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            is_user=True,
        )

        serializer.save(user=user)

        r_user=Users.objects.get(user=user)
        r_user.referred_by_id=r_code.user
        r_user.save()
        



        return Response({'Success': True, 'Code': 200, 'message': 'User created successfully.'}, status=HTTP_201_CREATED)
    else:
        return Response({'Success': False, 'Code': 400, 'message': serializer.errors}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def User_signup_view(request):
    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        email = request.data['email']

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return Response({'Success': False, 'Code': 400, 'message': 'Email already exists.'}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            username=request.data['username'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            is_user=True,
        )

        driver = serializer.save(user=user)

        return Response({'Success': True, 'Code': 200, 'message': 'User created successfully.'}, status=HTTP_201_CREATED)
    else:
        return Response({'Success': False, 'Code': 400, 'message': serializer.errors}, status=HTTP_400_BAD_REQUEST)



# @api_view(['GET', 'POST'])
# def profile_list(request):
#     if request.method == 'GET':
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)
@api_view(['POST'])
def create_profile(request, id):
    try:
        user = User.objects.get(pk=id)
        print(user)
    except Users.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
####buy policy
@api_view(['POST'])
def referral_points(request,pk):
    try:
        user=User.objects.get(id=pk)
        print(user)
    except:
        return Response({'Success': False, 'Code': 400}, status=HTTP_400_BAD_REQUEST)
    user2=Users.objects.get(user_id=user)
    referred_users=Users.objects.filter(referred_by_id=user)
    count=referred_users.count()
    points=count*2
    serializer=ReferredUserSerializer(referred_users,many=True)
    return Response({'Success': True, 'Code': 200, 'referred_users': serializer.data, "Loyalty_points":points}, status=HTTP_200_OK)


### buy policy
@api_view(['POST'])
def user_policy_create_view(request):
    serializer = UserPolicySerializer(data=request.data)
    if serializer.is_valid():
        is_draft = serializer.validated_data.get('is_draft')
        if is_draft:
            print('what')
            # Create a draft employee
            userpolicy = serializer.save()
            return Response({'success': True, 'code': HTTP_200_OK, 'message': 'Draft UserPolicy Created Successfully'}, status=HTTP_200_OK)
        else:
            print("whats_up")
            user = serializer.data.get('user')
            frequency = serializer.data.get('frequency')
            premium = serializer.data.get('premium')
            next_premium = serializer.data.get('next_premium')
            print('tf')
            policy_id=serializer.data.get('policy_id')
            print(policy_id)
            postal_address = serializer.data.get('postal_address')
            telephone_number = serializer.data.get('telephone_number')
            email = serializer.data.get('email')
            pin = serializer.data.get('pin')
            life_assured = serializer.data.get('life_assured')
            country = serializer.data.get('country')
            nationality = serializer.data.get('nationality')
            marital_status = serializer.data.get('marital_status')
            resident_country = serializer.data.get('resident_country')
            sum_assured = serializer.data.get('sum_assured')
            status = serializer.data.get('status')
            dob = serializer.data.get('dob')
            print(dob)
            full_name = serializer.data.get('full_name')

            today = datetime.date.today().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4().fields[-1])[:8]
            policy_number=f'B-{today}-{unique_id}'
            print(policy_number)
            policyduration=Policy.objects.get(id=policy_id).policy_duration
            print(policyduration)
            if frequency=='monthly':
                n_premium=(float(sum_assured)/float(policyduration))
                premium=(n_premium/12)
            if frequency=='quarterly':
                n_premium=(float(sum_assured)/float(policyduration))
                premium=(n_premium/12)
                premium=premium*4
            if frequency=='semi-annually':
                n_premium=(float(sum_assured)/float(policyduration))
                premium=(n_premium/12)
                premium=premium*6
            if frequency=='annually':
                n_premium=(float(sum_assured)/float(policyduration))
                premium=(n_premium/12)
                premium=premium*12

            next_premium=premium * 0.8

            print("hello")


            userpolicy = UserPolicy.objects.create(Policy_number=policy_number,user_id=user,frequency=frequency,premium=premium, next_premium=next_premium,policy_id_id=policy_id, postal_address=postal_address,
            telephone_number=telephone_number,email=email, pin=pin,life_assured=life_assured,country=country,
            nationality=nationality,marital_status=marital_status,resident_country=resident_country,sum_assured=sum_assured,
            status=status,dob=dob,full_name=full_name)

            policy2=UserPolicySerializer(userpolicy)

            return Response({'success': True, 'code': HTTP_200_OK, 'message': 'Policy Created Successfully','policy':policy2.data}, status=HTTP_200_OK)

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

#Get users Policies

@api_view(['GET'])
def get_users_policy(request, pk):
    try:
        policies = UserPolicy.objects.filter(user_id=pk)
        serializer = UserPolicySerializer2(policies, many=True)
        return Response({"user_policies":serializer.data})
    except:
        return Response(status=404)
    

###generate user referral url###



###policy types
@api_view(['POST'])
def create_policy_type(request):
    serializer = PolicyTypeSerializer(data=request.data)
    if serializer.is_valid():
        policy_type = serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_policy_type(request, pk):
    try:
        policy_type = PolicyTypes.objects.get(pk=pk)
        serializer = PolicyTypeSerializer(policy_type)
        return Response(serializer.data)
    except PolicyTypes.DoesNotExist:
        return Response(status=404)

@api_view(['PUT'])
def update_policy_type(request, pk):
    try:
        policy_type = PolicyTypes.objects.get(pk=pk)
        serializer = PolicyTypeSerializer(policy_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except PolicyTypes.DoesNotExist:
        return Response(status=404)

@api_view(['DELETE'])
def delete_policy_type(request, pk):
    try:
        policy_type = PolicyTypes.objects.get(pk=pk)
        policy_type.delete()
        return Response(status=204)
    except PolicyTypes.DoesNotExist:
        return Response(status=404)


####policy

###policy types
@api_view(['POST'])
def create_policy(request):
    serializer = PolicySerializer(data=request.data)
    if serializer.is_valid():
        policy = serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_policy(request, pk):
    try:
        policy = Policy.objects.get(pk=pk)
        serializer = PolicySerializer(policy)
        return Response(serializer.data)
    except Policy.DoesNotExist:
        return Response(status=404)

@api_view(['GET'])
def get_all_policy(request):
    try:
        policy = Policy.objects.all()
        serializer = PolicySerializer(policy, many=True)
        return Response(serializer.data)
    except Policy.DoesNotExist:
        return Response(status=404)

@api_view(['GET'])
def get_user_details(request,pk):
    try:
        user = Users.objects.get(pk=pk)
        serializer = ReferredUserSerializer(user)
        return Response(serializer.data)
    except Policy.DoesNotExist:
        return Response(status=404)

@api_view(['GET'])
def get_user_policies(request,pk):
    try:
        user = Users.objects.get(pk=pk)
        serializer = UserPolicySerializer(user, many=True)
        return Response(serializer.data)
    except Policy.DoesNotExist:
        return Response(status=404)

@api_view(['PUT'])
def update_policy(request, pk):
    try:
        policy = Policy.objects.get(pk=pk)
        serializer = PolicySerializer(policy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Policy.DoesNotExist:
        return Response(status=404)

@api_view(['PUT'])
def update_user_info(request, pk):
    try:
        policy = Users.objects.get(pk=pk)
        serializer = UsersSerializer(policy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Users.DoesNotExist:
        return Response(status=404)

@api_view(['DELETE'])
def delete_policy(request, pk):
    try:
        policy = Policy.objects.get(pk=pk)
        policy.delete()
        return Response(status=204)
    except Policy.DoesNotExist:
        return Response(status=404)
    

def create_password(short_code, pass_key):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        data = short_code + pass_key + timestamp
        encoded = base64.b64encode(data.encode("utf-8"))
        return encoded.decode("utf-8")

def generate_access_token(consumer_key, consumer_secret):
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        auth_string = consumer_key + ":" + consumer_secret
        base64_auth_string = base64.b64encode(auth_string.encode()).decode()

        headers = {
            "Authorization": "Basic " + base64_auth_string,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        access_token = response.json()["access_token"]
        return access_token

    


@api_view(['POST'])
def call_back(request): 
    print('This is starting')
    response_data=(request.data)
    print(request.data)
    # mpesa_receipt_number = response_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    # result_desc = response_data['Body']['stkCallback']['ResultDesc']
    # amount = response_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    # transaction_date = response_data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
    # checkout_request_id = response_data['Body']['stkCallback']['CheckoutRequestID']
    print(request.data['Body']['stkCallback']['ResultDesc'])

    


    # transaction=Transaction.objects.get(checkout_request_id=checkout_request_id)
    # if mpesa_receipt_number == None:
    #     transaction.status=False
    # else:
    #     transaction.status=True
    #     transaction.save()
    # transaction.time_stamp = transaction_date
    # transaction.amount = amount
    # transaction.result_description = result_desc
    # transaction.mpesa_receipt_number = mpesa_receipt_number
    # transaction.save()
    
    return Response(request.data)


@api_view(['POST'])
def stk_request(request):
    
    token = request.headers["Authorization"]

    token = token.split(" ")[1]
    decoded_token = AccessToken(token)
    decoded_payload = decoded_token.payload['user_id']
    print (decoded_payload)
    user=decoded_payload

    data = request.data
    phone = data.get('phone')
    amount = data.get('amount')

    transaction=MpesaService(user,amount,phone)
    resp=transaction.perform_full_transaction()
    
    print(resp)
    if "errorCode" in resp:
        return Response({"success":False,"message":"Push Not sent successfully"})
    else:
        checkout_id=resp['CheckoutRequestID']
        transaction=Transaction.objects.create(
            user_id=user,
            checkout_request_id=checkout_id,
            phone_number=phone

        )
        return Response({"success":True,"message":"Push sent successfully"})
    
    
    


 
    
  