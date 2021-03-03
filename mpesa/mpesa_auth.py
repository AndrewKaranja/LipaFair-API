import os
from base64 import b64encode

from M2Crypto import X509, RSA
from requests.auth import HTTPBasicAuth

from api import RequestSession
from lipafair import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MpesaBaseAuth(RequestSession):
    def __init__(self, env="sandbox", consumer_key=None, consumer_secret=None):
        super().__init__()
        self._env = env
        self._consumer_key = consumer_key
        self._secret_key = consumer_secret
        self._access_token = None

        if env == "sandbox":
            self._base_url = "https://sandbox.safaricom.co.ke"
            self.initiator_password = settings.MPESA_SANBOX_PASSWORD
            self.cert_path = os.path.join(BASE_DIR, 'mpesa/mpesa_sandbox_cert.cer')

        elif env == "live":
            self.initiator_password = settings.MPESA_SANBOX_PASSWORD
            self.cert_path = os.path.join(BASE_DIR, 'mpesa/mpesa_prod_cert.cer')
            self._base_url = "https://api.safaricom.co.ke"
        else:
            self._base_url = None

    def obtain_auth_token(self):
        """To make Mpesa API calls, you will need to authenticate your app. This method is used to fetch the access token
               required by Mpesa. Mpesa supports client_credentials grant type. To authorize your API calls to Mpesa,
               you will need a Basic Auth over HTTPS authorization token. The Basic Auth string is a base64 encoded string
               of your app's client key and client secret.

           **Args:**
               - env (str): Current app environment. Options: sandbox, live.
               - app_key (str): The app key obtained from the developer portal.
               - app_secret (str): The app key obtained from the developer portal.

           **Returns:**
               - access_token (str): This token is to be used with the Bearer header for further API calls to Mpesa.
        """

        auth_endpoint = "/oauth/v1/generate?grant_type=client_credentials"

        url = "{0}{1}".format(self._base_url, auth_endpoint)

        req = self.session.get(url=url, auth=HTTPBasicAuth(self._consumer_key, self._secret_key))
        print(req.json())
        if req.status_code == 200:

            self._access_token = req.json()['access_token']
            return self._access_token
        else:
            self._access_token = None
            return self._access_token

    def security_credential(self):

        cert_file = open(self.cert_path, 'rb')
        cert_data = cert_file.read()  # read certificate file
        cert_file.close()

        cert = X509.load_cert_string(cert_data)
        # pub_key = X509.load_cert_string(cert_data)
        pub_key = cert.get_pubkey()
        rsa_key = pub_key.get_rsa()
        cipher = rsa_key.public_encrypt(bytes(str(settings.B2C_INITIATOR_PASSWORD), "utf-8"), RSA.pkcs1_padding)
        return b64encode(cipher)
