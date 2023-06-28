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


# @api_view(['POST'])
# def employees_edit_view(request, id):
#     try:
#         employee = Employees.objects.get(id=id)
#     except Employees.DoesNotExist:
#         return Response({'message': 'Employee does not exist'}, status=HTTP_404_NOT_FOUND)
    
#     serializer = Employeeserializer(employee, data=request.data, partial=True)

#     if serializer.is_valid():        
#         if employee.is_draft and 'is_draft' in request.data and request.data['is_draft']:
#             serializer.save() 
#             return Response({'Success': 'True', 'Code': 200, 'message': 'Employee Draft Update Successful'}, status=HTTP_200_OK)
            
#         elif employee.is_draft and 'is_draft' in request.data and not request.data['is_draft']:
#             serializer.save()
#             email = serializer.data.get('work_email')
#             first_name = serializer.data.get('first_name')
#             last_name = serializer.data.get('last_name')
#             password = get_random_string(10).lower()

#             try:
#                 Users.objects.get(email=email)
#                 return Response({'success': False, 'code': HTTP_400_BAD_REQUEST, 'message': 'email already exists'}, status=HTTP_400_BAD_REQUEST)
#             except ObjectDoesNotExist:
#                 try:
#                     User.objects.create_user(
#                         username=email, password=password, email=email)
#                 except:
#                     return Response({'success': False, 'code': HTTP_400_BAD_REQUEST, 'message': 'User with the email already exist'}, status=HTTP_400_BAD_REQUEST)

#                 my_form = Users(email=email,
#                                 phone_number=employee.phone_number,
#                                 first_name=first_name,
#                                 last_name=last_name,
#                                 user_type=employee.user_type,
#                                 modules='[]',
#                                 roles=employee.roles.id,
#                                 profile=employee.profile.id,
#                                 first_account=True,
#                                 company_id=employee.company_id,
#                                 status=employee.status)
#                 my_form.save()

#                 user_id = (Users.objects.last()).id
#                 employee.user_id=user_id
#                 employee.save()

#                 user2=User.objects.get(email=email)
#                 if employee.status =='Inactive':
#                     user2.is_active=False
#                     user2.save()


#                 company = employee.company_id
#                 actioned_by = employee.actioned_by_id

#                 modules = f'HR'
#                 activity = f'Created Employee user_id {user_id}, {email}'

#                 add_system_logs(company, actioned_by=actioned_by,
#                                 activity=activity, modules=modules)

#                 message = f'Welcome to Tiger your login credentials are <br> email: {email} <br> password {password} '
#                 subject = "Account Creation"
#                 send_email(email, message, subject, company)
            
        
#             return Response({'Success': 'True', 'Code': 200, 'message': 'Employee Draft Update Successful'}, status=HTTP_200_OK)
#         else:
#             email = serializer.data.get('work_email')
#             phone_number = serializer.data.get('phone_number')
#             first_name = serializer.data.get('first_name')
#             last_name = serializer.data.get('last_name')
#             user_type = serializer.data.get('user_type')
#             team = serializer.data.get('team')
#             roles = serializer.data.get('roles')
#             profile = serializer.data.get('profile')
#             company = serializer.data.get('company')
#             status = serializer.data.get('status')
#             attributes = serializer.data.get('attributes')
#             user = Employees.objects.get(pk=id).user_id
#             print(user)
#             try:
#                 n = Employees.objects.get(~Q(id=id), work_email=email)
#                 return Response({'Success': 'False', 'Code': 400, 'message': 'Email Already Exists'}, status=HTTP_404_NOT_FOUND)
#             except ObjectDoesNotExist:
#                 u = Users.objects.get(id=user)
#                 print(u)
#                 u.email = email
#                 u.phone_number = phone_number
#                 u.first_name = first_name
#                 u.last_name = last_name
#                 u.user_type = user_type
#                 u.roles = roles
#                 u.profile = profile
#                 u.status = status
#                 u.save()

#                 serializer = Employees.objects.get(pk=id)

#                 data = Employeeserializer(
#                     instance=serializer, data=request.data)
#                 if data.is_valid():
#                     data.save()

#                     # team = []

#                     # for team_id in request.data.get('team'):
#                     #     try:
#                     #         uteam = Teams.objects.get(id=team_id)
#                     #         team.append(uteam)
#                     #     except Teams.DoesNotExist:
#                     #         raise NotFound()

#                     breaks = []

#                     # for break_id in serializer.data.get('breaks'):
#                     #     try:
#                     #         break_schedule = Breaks.objects.get(id=break_id)
#                     #         breaks.append(break_schedule)
#                     #     except Teams.DoesNotExist:
#                     #         raise NotFound()


#                     company = data.data.get('company')
#                     actioned_by = data.data.get('actioned_by')

#                     modules = f'HR'
#                     activity = f'Edited Employee  {id}, {email}'

#                     add_system_logs(company, actioned_by=actioned_by,
#                                     activity=activity, modules=modules)
#             return Response({'Success': 'True', 'Code': 200, 'message': 'Employee Update Successful'}, status=HTTP_200_OK)
#     return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


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
    
# ###mpesa###
# def create_password(self, short_code, pass_key):
#         timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#         data = short_code + pass_key + timestamp
#         encoded = base64.b64encode(data.encode("utf-8"))
#         return encoded.decode("utf-8")


# class MpesaService():
#     BASE_URL = "https://sandbox.safaricom.co.ke"
#     CONSUMER_KEY = 'wPcudd67umTpFGoO09TOaEPVwyePSPNf'
#     CONSUMER_SECRET = 'n5pPou2lA3C3lZhh'
#     PASS_KEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'


#     def base_64_encode(self, consumer_key, consumer_secret):
#         """
#         Returns a base64 encoded string
#         """
#         data = consumer_key + ":" + consumer_secret
#         encoded = base64.b64encode(data.encode("utf-8"))
#         return encoded.decode("utf-8")
    
#     # def get_access_token(self):
#     #     url = self.BASE_URL + "/oauth/v1/generate?grant_type=client_credentials"
#     #     headers = {
#     #             "Authorization": "Basic " + self.base_64_encode(self.CONSUMER_KEY, self.CONSUMER_SECRET)
#     #     }

#     #     response = requests.get(url, headers=headers)

#     #     # response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Bearer d1BjdWRkNjd1bVRwRkdvTzA5VE9hRVBWd3llUFNQTmY6bjVwUG91MmxBM0MzbFpoaA==' })
#     #     # print(response.text.encode('utf8'))

#     #     return response.json()["access_token"]

#     def generate_access_token(consumer_key, consumer_secret):
#         url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
#         auth_string = consumer_key + ":" + consumer_secret
#         base64_auth_string = base64.b64encode(auth_string.encode()).decode()

#         headers = {
#             "Authorization": "Basic " + base64_auth_string,
#             "Content-Type": "application/json"
#         }

#         response = requests.get(url, headers=headers)
#         access_token = response.json()["access_token"]
#         return access_token

#     # Replace with your actual Consumer Key and Consumer Secret
#     consumer_key = "wPcudd67umTpFGoO09TOaEPVwyePSPNf"
#     consumer_secret = "n5pPou2lA3C3lZhh"

#     access_token = generate_access_token(consumer_key, consumer_secret)
#     print("Access Token:", access_token)
    
#     def create_password(self, short_code, pass_key):
#         timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#         data = short_code + pass_key + timestamp
#         encoded = base64.b64encode(data.encode("utf-8"))
#         return encoded.decode("utf-8")

#     def send_stk_push(self,amount,phone ):
        
#         url = self.BASE_URL + "/mpesa/stkpush/v2/processrequest"
#         consumer_key = "wPcudd67umTpFGoO09TOaEPVwyePSPNf"
#         consumer_secret = "n5pPou2lA3C3lZhh"

#         access_token = self.generate_access_token(consumer_key, consumer_secret)
#         access_token = self.access_token

#         headers = {
#                 "Authorization": "Bearer " + access_token,
#                 "Content-Type": "application/json"
#         }

#         request = {
#                 "BusinessShortCode": "174379",
#                 "Password": self.create_password("174379", self.PASS_KEY),
#                 "Timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
#                 "TransactionType": "CustomerPayBillOnline",
#                 "Amount": amount,
#                 "PartyA": phone,
#                 "PartyB": "174379",
#                 "PhoneNumber": phone,
#                 "CallBackURL": "",
#                 "AccountReference": "Test",
#                 "TransactionDesc": "Test"
#         }

#         response = requests.post(url, json=request, headers=headers)
#         print(response)
#         return response.json()

#     def get_stk_push_status(self, checkout_request_id):
#         url = self.BASE_URL + "/mpesa/stkpushquery/v1/query"
#         access_token = self.generate_access_token()

#         headers = {
#                 "Authorization": "Bearer " + access_token,
#                 "Content-Type": "application/json"
#         }

#         request = {
#                 "BusinessShortCode": "174379",
#                 "Password": self.create_password("174379", self.PASS_KEY),
#                 "Timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
#                 "CheckoutRequestID": checkout_request_id
#         }

#         response = requests.post(url, json=request, headers=headers)
#         return response.json()

#     def perform_full_transaction(self, amount, phone):
#         response = self.send_stk_push(amount, phone)
#         print(response)
#         checkout_request_id = response["CheckoutRequestID"]
#         import time
#         while True:
#             print(response)
#             response = self.get_stk_push_status(checkout_request_id)

#             try:
#                 if response["errorMessage"]:
#                     continue
#             except KeyError:
#                 #if response["resultDesc"} contains cancelled
#                 if response["ResultDesc"] == "Request cancelled by user":
#                     return False
#                 elif response["ResultDesc"] == "The service request is processed successfully.":
#                     return True
#                 else:
#                     return response
#             time.sleep(5)


# mpesa_service = MpesaService()

# print(mpesa_service.perform_full_transaction(1, "254791315571"))







# def get_access_token():
#     url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
#     consumer_key_secret = settings.MPESA_CONSUMER_KEY + ":" + settings.MPESA_CONSUMER_SECRET
#     #base64 encode the consumer_key and consumer_secret
#     consumer_key_secret = base64.b64encode(consumer_key_secret.encode("utf-8"))
#     headers = {
#             'Authorization': 'Basic ' + consumer_key_secret.decode("utf-8"),
#             'Content-Type': 'application/json'
#         }

#     response = requests.request("GET", url, headers=headers)
#     return response.json()['access_token']
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
    
    
    


 
    
  