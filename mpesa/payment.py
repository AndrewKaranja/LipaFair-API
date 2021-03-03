from lipafair import settings
from mpesa.mpesa_express import MpesaExpress
from mpesa.utils import CleanPhoneNumber


class MpesaSTKPushTxn(object):
    def __init__(self, phone_number=None, amount=None, reference_code=None):
        self.mpesa_consumer_key = settings.MPESA_CONSUMER_SANDBOX
        self.mpesa_secret_key = settings.MPESA_SECRET_SANDBOX

        self.phone_number = CleanPhoneNumber(phone_number).sanitize_phone_number()
        self.amount = int(amount)

        self.callback_url = ""
        self.short_code = settings.MPESA_SHORT_CODE_SANDBOX
        self.lnm_passkey = settings.LNM_PASSKEY_SANDBOX
        self.reference_code = reference_code

    def initiate_txn(self):
        mpesa_api = MpesaExpress(
            env=settings.MPESA_ENV,
            consumer_key=self.mpesa_consumer_key,
            consumer_secret=self.mpesa_secret_key
        )

        return mpesa_api.stk_push(
            business_shortcode=self.short_code,
            lnm_passkey=self.lnm_passkey,
            amount=self.amount,
            callback_url=self.callback_url,
            phone_number=self.phone_number,
            description='water units',
            reference_code=self.reference_code

        )
