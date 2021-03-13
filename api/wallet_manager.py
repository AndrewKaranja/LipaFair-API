from rest_framework import status

from api import RequestSession
from api.auth import BearerTokenAuth
from lipafair import settings


class StoreWalletManager(RequestSession):
    def __init__(self):
        super().__init__()
        self.email = settings.FIREBASE_FUNC_USERNAME
        self.password = settings.FIREBASE_FUNC_PASSWORD
        self.auth_endpoint = settings.FIREBASE_FUNC_AUTH_URL
        self.wallet_url = settings.UPDATE_STORE_WALLET_ENDPOINT

    def generate_auth_token(self):
        payload = {
            "email": self.email,
            "password": self.password
        }

        req = self.session.post(url=self.auth_endpoint, data=payload)

        if req.status_code == status.HTTP_200_OK:
            return req.json()['token']
        else:
            return req.json()

    def update_wallet(self, payload):
        token = self.generate_auth_token()

        if token is not None:
            # make the request
            req = self.session.post(url=self.wallet_url, json=payload, auth=BearerTokenAuth(token=token))
            if req.status_code == status.HTTP_200_OK:
                return req.json()
            else:
                return req.json()
        else:
            return {
                "message": "Error occurred while generating auth token"
            }



