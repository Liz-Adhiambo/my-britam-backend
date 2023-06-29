import base64
import requests
import datetime
import time
from britam_backend import settings

class MpesaService():
    BASE_URL = settings.BASE_URL 
    CONSUMER_KEY = settings.CONSUMER_KEY
    CONSUMER_SECRET = settings.CONSUMER_SECRET
    PASS_KEY = settings.PASS_KEY
    user = ""
    amount = ""
    phone = ""

    def __init__(self, user, amount, phone):
        self.user = user
        self.amount = amount
        self.phone = phone

    def base_64_encode(self, consumer_key, consumer_secret):
        """
        Returns a base64 encoded string
        """
        data = consumer_key + ":" + consumer_secret
        encoded = base64.b64encode(data.encode("utf-8"))
        return encoded.decode("utf-8")

    def get_access_token(self):
        url = self.BASE_URL + "/oauth/v1/generate?grant_type=client_credentials"
        headers = {
                "Authorization": "Basic " + self.base_64_encode(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        }

        response = requests.get(url, headers=headers)

        return response.json()["access_token"]

    def create_password(self, short_code, pass_key):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        data = short_code + pass_key + timestamp
        encoded = base64.b64encode(data.encode("utf-8"))
        return encoded.decode("utf-8")

    def send_stk_push(self, amount, phone):
        url = self.BASE_URL + "/mpesa/stkpush/v1/processrequest"
        access_token = self.get_access_token()

        headers = {
                "Authorization": "Bearer " + access_token,
                "Content-Type": "application/json"
        }

        # request = {
        #         "BusinessShortCode": "174379",
        #         "Password": self.create_password("174379", self.PASS_KEY),
        #         "Timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        #         "TransactionType": "CustomerPayBillOnline",
        #         "Amount": amount,
        #         "PartyA": phone,
        #         "PartyB": "174379",
        #         "PhoneNumber": phone,
        #         "CallBackURL": "https://ef5a-62-8-70-50.ngrok-free.app/api/v1/callback",
        #         "AccountReference": "Test",
        #         "TransactionDesc": "Test"
        # }
        request={
                "BusinessShortCode": 174379,
                "Password": self.create_password("174379", self.PASS_KEY),
                "Timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone,
                "PartyB": 174379,
                "PhoneNumber": phone,
                "CallBackURL": "https://my-britam-backend-production.up.railway.app/api/v1/callback",
                "AccountReference": "CompanyXLTD",
                "TransactionDesc": "Payment of X" 
            }

        response = requests.post(url, json=request, headers=headers)
        print(response.json())
        return response.json()

    def get_stk_push_status(self, checkout_request_id):
        url = self.BASE_URL + "/mpesa/stkpushquery/v1/query"
        access_token = self.get_access_token()

        headers = {
                "Authorization": "Bearer " + access_token,
                "Content-Type": "application/json"
        }

        request = {
                "BusinessShortCode": "174379",
                "Password": self.create_password("174379", self.PASS_KEY),
                "Timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                "CheckoutRequestID": checkout_request_id
        }

        response = requests.post(url, json=request, headers=headers)
        return response.json()

    def perform_full_transaction(self):
        return self.send_stk_push(self.amount, self.phone)


# mpesa_service = MpesaService()

# print(mpesa_service.perform_full_transaction(1, "254112159579"))