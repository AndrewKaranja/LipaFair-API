from rest_framework import serializers

from api.models import *


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class MpesaTransactionSerializer(serializers.ModelSerializer):
    txn_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = MpesaTransaction
        fields = '__all__'