from django.contrib import admin

# Register your models here.
from api.models import *


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['wallet_id', 'user_id', 'current_balance', 'last_updated']

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'txn_id',
        'mpesa_receipt',
        'amount',
        'reason',
        'account',
        'txn_type',
        'status',
        'txn_date'
    ]

