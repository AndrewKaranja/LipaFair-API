from api.auth import BearerTokenAuth
from lipafair import settings
from mpesa.mpesa_auth import MpesaBaseAuth
from mpesa.utils import CleanPhoneNumber


class B2C(MpesaBaseAuth):
    def __init__(self, env='sandbox'):
        if env == 'sandbox':
            super(B2C, self).__init__(env=env, consumer_key=settings.MPESA_CONSUMER_SANDBOX,
                                      consumer_secret=settings.MPESA_SECRET_SANDBOX)
            self.callback = settings.B2C_SANDBOX_CALLBACK_URL
            self.party_a = settings.B2C_SANDBOX_PAYBILL
            self.initiator_name = settings.B2C_SANDBOX_INITIATOR_NAME
            self.timeout_url = settings.B2C_SANDBOX_TIMEOUT_URL
        # else:
            # super(B2C, self).__init__(env=env, consumer_key=settings.MPESA_CONSUMER_B2C_LIVE,
            #                           consumer_secret=settings.MPESA_SECRET_B2C_LIVE)
            # self.callback = settings.B2C_CALLBACK_URL
            # self.party_a = settings.B2C_PAYBILL
            # self.initiator_name = settings.B2C_INITIATOR_NAME
            # self.timeout_url = settings.B2C_TIMEOUT_URL

        self.obtain_auth_token()


    def initiate_b2c(self, phone_number, amount, occasion):
        headers = {
            'Content-Type': 'application/json'
        }
        auth = BearerTokenAuth(self._access_token)
        party_b = CleanPhoneNumber(phone_number=phone_number).sanitize_phone_number()

        payload = {
            "InitiatorName": self.initiator_name,
            "SecurityCredential": str(self.security_credential(), 'utf-8'),
            "CommandID": "BusinessPayment",
            "Amount": str(amount),
            "PartyA": self.party_a,
            "PartyB": party_b,
            "Remarks": "Salary payments",
            "QueueTimeOutURL": settings.B2C_SANDBOX_TIMEOUT_URL,
            "ResultURL": self.callback,
            "Occassion": occasion
        }
        print(payload)
        url = f"{self._base_url}/mpesa/b2c/v1/paymentrequest"
        req = self.session.post(url=url, json=payload, headers=headers, auth=auth)
        return req.json()

if __name__ == '__main__':
   b2c = B2C()

   res = b2c.initiate_b2c(phone_number=settings.MPESA_B2C_TEST_MSISDN, amount=10, occasion="payment")
   print(res)