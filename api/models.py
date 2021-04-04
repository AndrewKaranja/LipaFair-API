from _decimal import Decimal

from django.db import models

# Create your models here.
from api.wallet_manager import StoreWalletManager
from mpesa.payment_signals import stk_payment_completed, checkout_from_wallet_completed, b2c_payment_completed


class Wallet(models.Model):
    #same as docKey
    wallet_id = models.CharField(max_length=128,)
    user_id = models.CharField(max_length=128, unique=True)
    current_balance = models.DecimalField(max_digits=9, decimal_places=2)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wallet_id

class MpesaTransaction(models.Model):
    user_id = models.CharField(max_length=128, null=True,blank=True)
    txn_id = models.CharField(max_length=128, )
    mpesa_receipt = models.CharField(max_length=32, blank=True, null=True,default="")
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    reason = models.CharField(max_length=128, )
    account = models.CharField(max_length=128, default="")
    TXN_TYPES = (
        ('WalletTopUp', 'WalletTopUp'),
        ('Checkout', 'Checkout')
    )
    txn_type = models.CharField(max_length=32, choices=TXN_TYPES)

    TXN_STATUS = (
        ('pending', 'pending'),
        ('failed', 'failed'),
        ('success', 'success'),
    )
    status = models.CharField(max_length=32, choices=TXN_STATUS, default=TXN_STATUS[0][0])
    txn_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('txn_date', )

    def __str__(self):
        return self.txn_id

class WalletTransaction(models.Model):
    user_id = models.CharField(max_length=128, null=False, blank=False)
    txn_id = models.CharField(max_length=128, null=False, blank=False)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    account = models.CharField(max_length=128, )
    txn_type = models.CharField(max_length=32, default="CheckoutFromWallet")
    TXN_STATUS = (
        ('pending', 'pending'),
        ('failed', 'failed'),
        ('success', 'success'),
    )
    status = models.CharField(max_length=32, choices=TXN_STATUS, default=TXN_STATUS[0][0])
    txn_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('txn_date', )

    def __str__(self):
        return self.txn_id


class B2CWithdrawalRequest(models.Model):
    account_no = models.CharField(max_length=32, null=False, blank=False)
    txn_id = models.CharField(max_length=256, )
    txn_ref = models.CharField(max_length=128, null=True, blank=True)
    amount = models.CharField(max_length=20, )
    phone_number = models.CharField(max_length=20, )
    customer_name = models.CharField(max_length=128, null=True, blank=True)
    remarks = models.CharField(max_length=140, default="Wallet Withdrawal")
    status = models.CharField(max_length=32, default="pending")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.txn_id


def on_stk_checkout_completed(sender, **kwargs):
    transaction = kwargs.get('transaction')
    txn_type = transaction.txn_type


    if txn_type == 'WalletTopUp':
        #updated the wallet.
        wallet = Wallet.objects.get(wallet_id=transaction.account)
        wallet.current_balance += Decimal(transaction.amount)
        wallet.save()
    else:
        #implement other checkout here
        payload = {
            "accountNo": str(transaction.account),
            "amount": int(transaction.amount),
            "transactionType": "credit"
        }

        wallet_manager = StoreWalletManager()
        print(wallet_manager.update_wallet(payload=payload))


stk_payment_completed.connect(on_stk_checkout_completed)


def on_checkout_from_wallet_completed(sender, **kwargs):
    transaction = kwargs.get('transaction')

    client_wallet = kwargs.get('client_wallet')
    client_wallet.current_balance -= Decimal(transaction.amount)
    client_wallet.save()

    payload = {
        "accountNo": str(transaction.account),
        "amount": int(transaction.amount),
        "transactionType": "credit"
    }

    wallet_manager = StoreWalletManager()
    print(wallet_manager.update_wallet(payload=payload))

checkout_from_wallet_completed.connect(on_checkout_from_wallet_completed)


def on_wallet_withdrawal_completed(sender, **kwargs):
    transaction = kwargs.get('transaction')
    payload = {
        "accountNo": str(transaction.account_no),
        "amount": int(transaction.amount),
        "transactionType": "debit"
    }
    wallet_manager = StoreWalletManager()
    print(wallet_manager.update_wallet(payload=payload))

b2c_payment_completed.connect(on_wallet_withdrawal_completed)