from django.contrib import admin

# Register your models here.
from api.models import *


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['wallet_id', 'user_id', 'current_balance', 'last_updated']

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'user_id',
        'txn_id',
        'mpesa_receipt',
        'amount',
        'reason',
        'account',
        'txn_type',
        'status',
        'txn_date'
    ]

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WalletTransaction._meta.get_fields()][1:]

@admin.register(B2CWithdrawalRequest)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in B2CWithdrawalRequest._meta.get_fields()][1:]

