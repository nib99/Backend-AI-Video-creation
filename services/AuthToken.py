import requests
import json
from service import applyFabricTokenService
from utils import tools
from config import env

class AuthTokenService:
    def __init__(self, BASE_URL, fabricAppId, appSecret, merchantAppId):
        self.BASE_URL = BASE_URL
        self.fabricAppId = fabricAppId
        self.appSecret = appSecret
        self.merchantAppId = merchantAppId
   
    def auth_token(self, app_token):
        """
        This method fetches the auth token by calling ApplyFabricTokenService
        and then requests the auth token.
        """
        print("Token:", app_token)
        # Step 1: Apply Fabric Token
        apply_fabric_token_service = applyFabricTokenService.ApplyFabricTokenService(self.BASE_URL, self.fabricAppId, self.appSecret, self.merchantAppId)
        fabric_token_response = apply_fabric_token_service.applyFabricToken()
        fabric_token = fabric_token_response["token"]  # Extract the fabric token from the response
       
        # Step 2: Request the Auth Token
        auth_token_result = self.request_auth_token(fabric_token, app_token)
        return auth_token_result
   
    def request_auth_token(self, fabric_token, app_token):
        """
        This method requests the Auth Token from the endpoint using the
        obtained fabric token and app token.
        """
        headers = {
            "Content-Type": "application/json",
            "X-APP-Key": self.fabricAppId,
            "Authorization": fabric_token
        }
       
        # Create the request object
        request_object = self.create_request_object(app_token)
       
        # Make the request to get the auth token
        response = requests.post(url=self.BASE_URL + "/payment/v1/auth/authToken", headers=headers, json=request_object, verify=False)
       
        # Return the response in JSON format
        return response.json()
   
    def create_request_object(self, app_token):
        """
        Creates the request object required for the Auth Token request.
        """
        req = {
            "timestamp": tools.create_timestamp(),
            "nonce_str": tools.create_nonce_str(),
            "method": "payment.authtoken",
            "version": "1.0",
        }
       
        biz = {
            "access_token": app_token,
            "trade_type": "InApp",
            "appid": self.merchantAppId,
            "resource_type": "OpenId"
        }
       
        req["biz_content"] = biz
        req["sign"] = tools.sign_request_object(req)
        req["sign_type"] = "SHA256WithRSA"
       
        print("Request Object:", json.dumps(req, indent=4))
       
        return req
