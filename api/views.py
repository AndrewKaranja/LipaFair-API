from _decimal import Decimal

from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from api.models import Wallet, MpesaTransaction
from api.serializers import WalletSerializer, MpesaTransactionSerializer
from mpesa.payment import MpesaSTKPushTxn
from mpesa.payment_signals import stk_payment_completed


class WalletListCreatePIView(generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        return get_object_or_404(Wallet, user_id=user_id)


class TopUpWalletRequest(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        wallet_id = data.get('wallet_id', '')
        amount = data.get('amount', '')
        phone_number = data.get('phone_number', '')
        stk_request = MpesaSTKPushTxn(phone_number=phone_number, amount=amount, reference_code=wallet_id,
                                      callback_url="https://lipafair.herokuapp.com/api/wallettopup-callback/")
        response = dict(stk_request.initiate_txn())
        print(response)
        if response.get('ResponseCode') == '0':
            txn = MpesaTransaction.objects.create(
                txn_id=response.get('CheckoutRequestID'),
                reason="Topping up the wallet",
                amount=Decimal(amount),
                account=wallet_id,
                txn_type="WalletTopUp"

            )
            txn.save()
            return Response(status=status.HTTP_200_OK, data={
                'message': "Request sent successfully check your phone to complete payment"
            })


        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'message': 'Error occurred while processing your request. Please try again later'}
                            )


class TopUpWalletCallback(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        stk_body = data.get('Body').get('stkCallback')
        checkout_request_id = stk_body.get('CheckoutRequestID')
        mpesa_receipt = stk_body.get('CallbackMetadata').get('Item')[1].get('Value')
        result_code = stk_body.get('ResultCode')
        print(stk_body)
        try:
            payment = MpesaTransaction.objects.get(txn_id=checkout_request_id)
            if str(result_code) == '0':
                payment.mpesa_receipt = mpesa_receipt
                if payment.status == 'pending':
                    stk_payment_completed.send(sender=self.__class__, transaction=payment)

                payment.status = "success"
                payment.save()
            else:
                payment.status = 'failed'
                payment.save()
            return Response(status=status.HTTP_200_OK)
        except MpesaTransaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': "No transaction Record found"
            })


class DirectSTKCheckoutRequest(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        amount = data.get('amount', '')
        phone_number = data.get('phone_number', '')
        account = data.get('account', '')
        stk_request = MpesaSTKPushTxn(phone_number=phone_number, amount=amount, reference_code=account,
                                      callback_url="https://lipafair.herokuapp.com/api/stk-checkout-callback/")
        response = dict(stk_request.initiate_txn())

        if response.get('ResponseCode') == '0':
            txn = MpesaTransaction.objects.create(
                txn_id=response.get('CheckoutRequestID'),
                reason="Direct checkout",
                amount=Decimal(amount),
                account=phone_number,
                txn_type="Checkout"

            )
            txn.save()
            return Response(status=status.HTTP_200_OK, data={
                'message': "Request sent successfully check your phone to complete payment"
            })

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'message': 'Error occurred while processing your request. Please try again later'}
                            )


class DirectCheckoutSTKCallback(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        stk_body = data.get('Body').get('stkCallback')
        checkout_request_id = stk_body.get('CheckoutRequestID')
        mpesa_receipt = stk_body.get('CallbackMetadata').get('Item')[1].get('Value')
        result_code = stk_body.get('ResultCode')

        try:
            payment = MpesaTransaction.objects.get(txn_id=checkout_request_id)
            if str(result_code) == '0':
                payment.mpesa_receipt = mpesa_receipt
                if payment.status == 'pending':
                    stk_payment_completed.send(sender=self.__class__, transaction=payment)
                payment.status = "success"
                payment.save()
            else:
                payment.status = 'failed'
                payment.save()
            return Response(status=status.HTTP_200_OK)
        except MpesaTransaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': "No transaction Record found"
            })


class TransactionsListAPIView(generics.ListAPIView):
    serializer_class = MpesaTransactionSerializer

    def get_queryset(self):
        return MpesaTransaction.objects.filter(account=self.kwargs.get('wallet_id', '')).order_by('txn_date')
