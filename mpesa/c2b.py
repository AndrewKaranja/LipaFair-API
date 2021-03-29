import requests

from api.auth import BearerTokenAuth
from lipafair import settings
from mpesa.mpesa_auth import MpesaBaseAuth


class C2B(MpesaBaseAuth):
    def __init__(self, env='sandbox', consumer_key=None, consumer_secret=None):
        super(C2B, self).__init__(env=env, consumer_key=consumer_key, consumer_secret=consumer_secret)
        self.obtain_auth_token()

    def register(self, response_type=None, short_code=None, validation_url=None, confirmation_url=None):
        """This method uses Mpesa's C2B API to register validation and confirmation URLs on M-Pesa.
           **Args:**
               - shortcode (str): The short code of the organization. options: Cancelled, Completed
               - response_type (str): Default response type for timeout. Incase a tranaction times out, Mpesa will by default Complete or Cancel the transaction.
               - confirmation_url (str): Confirmation URL for the client.
               - validation_url (str): Validation URL for the client.
           **Returns:**
               - OriginatorConverstionID (str): The unique request ID for tracking a transaction.
               - ConversationID (str): The unique request ID returned by mpesa for each request made
               - ResponseDescription (str): Response Description message
        """

        payload = {
            "ShortCode": short_code,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url
        }

        headers = {
            'Content-Type': 'application/json'
        }

        resource_url = "{0}{1}".format(self._base_url, "/mpesa/c2b/v1/registerurl")
        req = requests.post(url=resource_url, headers=headers, auth=BearerTokenAuth(self._access_token), json=payload)

        return req.json()

    def simulate_c2b(self, short_code=None, command_id=None, amount=None, phone_number=None, bill_ref_no=None):
        """This method uses Mpesa's C2B API to simulate a C2B transaction.
            **Args:**
                - short_code (str): The short code of the organization.
                - command_id (str): Unique command for each transaction type. - CustomerPayBillOnline - CustomerBuyGoodsOnline.
                - amount (str): The amount being transacted
                - phone_number (str): Phone number (msisdn) initiating the transaction MSISDN(12 digits)
                - bill_ref_no: Optional Represents account_no
            **Returns:**
                - OriginatorConverstionID (str): The unique request ID for tracking a transaction.
                - ConversationID (str): The unique request ID returned by mpesa for each request made
                - ResponseDescription (str): Response Description message
        """

        endpoint = "/mpesa/c2b/v1/simulate"

        url = "{0}{1}".format(self._base_url, endpoint)
        headers = {
            "Content-Type": 'application/json'
        }

        payload = {
            "ShortCode": short_code,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": phone_number,
            "BillRefNumber": bill_ref_no
        }

        req = requests.post(url=url, headers=headers, auth=BearerTokenAuth(self._access_token), json=payload)

        return req.json()

if __name__ == '__main__':
    c2b = C2B(env="sandbox",consumer_key=settings.MPESA_CONSUMER_SANDBOX, consumer_secret=settings.MPESA_SECRET_SANDBOX)
    res = c2b.simulate_c2b(short_code=settings.B2C_SANDBOX_PAYBILL, command_id="CustomerPayBillOnline", amount=50, phone_number=settings.MPESA_B2C_TEST_MSISDN, bill_ref_no="Test")
    print(res)
