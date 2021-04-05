from rest_framework import status

from api import RequestSession
from api.auth import BearerTokenAuth
from lipafair import settings


class B2CTariffManager(RequestSession):
    def __init__(self):
        super().__init__()
        self.email = settings.FIREBASE_FUNC_USERNAME
        self.password = settings.FIREBASE_FUNC_PASSWORD
        self.auth_endpoint = settings.FIREBASE_FUNC_AUTH_URL
        self.tariff_url = settings.TARIFF_URL

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


    def get_charges(self, amount=None):
        token = self.generate_auth_token()
        charges = None
        if token is not None:
            req = self.session.get(url=self.tariff_url, auth=BearerTokenAuth(token=token))
            if req.status_code == status.HTTP_200_OK:
                data = req.json()
                for item in data:
                    if int(item.get('min')) <= int(amount) <= int(item.get('max')):
                        charges = int(item.get('charges'))

            else:
                charges = None
        return charges
