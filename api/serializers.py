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


class TransactionSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=128,)
    txn_id = serializers.CharField(max_length=128, )
    amount = serializers.DecimalField(decimal_places=2, max_digits=9)
    account = serializers.CharField(max_length=128, )
    txn_type = serializers.CharField(max_length=32,)
    status = serializers.CharField(max_length=32, )
    txn_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class B2CTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2CWithdrawalRequest
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = (
            'id',
            'coupon_id',
            'amount_off',
            'percent_off',
            'currency',
            'created',
            'duration',
            'duration_in_months',
            'name',
            'livemode',
            'max_redemptions',
            'times_redeemed',
            'redeem_by',
            'valid'

        )