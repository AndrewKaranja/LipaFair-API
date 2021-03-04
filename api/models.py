from django.db import models

# Create your models here.
class Wallet(models.Model):
    #same as docKey
    wallet_id = models.CharField(max_length=128,)
    user_id = models.CharField(max_length=128,)
    current_balance = models.DecimalField(max_digits=9, decimal_places=2)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wallet_id

class MpesaTransaction(models.Model):
    txn_id = models.CharField(max_length=128, )
    mpesa_receipt = models.CharField(max_length=32, blank=True, null=True)
    amount = models.PositiveIntegerField()
    reason = models.CharField(max_length=128, )
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

