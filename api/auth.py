import hashlib
import random

from requests.auth import AuthBase


class BearerTokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


def generate_otp_code():
    return str(random.randrange(100000, 999999))

