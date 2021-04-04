import uuid
from _decimal import Decimal

from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from api.models import Wallet, MpesaTransaction, WalletTransaction, B2CWithdrawalRequest
from api.serializers import WalletSerializer, MpesaTransactionSerializer, B2CTransactionSerializer
from api.tariffs import B2CTariffManager
from api.wallet_manager import StoreWalletManager
from lipafair import settings
from mpesa.b2c import B2C
from mpesa.payment import MpesaSTKPushTxn
from mpesa.payment_signals import stk_payment_completed, checkout_from_wallet_completed, b2c_payment_completed


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
        user_id = data.get('user_id', '')
        phone_number = data.get('phone_number', '')
        stk_request = MpesaSTKPushTxn(phone_number=phone_number, amount=amount, reference_code=wallet_id,
                                      callback_url="https://lipafair.herokuapp.com/api/wallettopup-callback/")
        response = dict(stk_request.initiate_txn())
        print(response)
        if response.get('ResponseCode') == '0':
            txn = MpesaTransaction.objects.create(
                user_id=user_id,
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
        user_id = data.get('user_id', '')
        phone_number = data.get('phone_number', '')
        account = data.get('account', '')
        stk_request = MpesaSTKPushTxn(phone_number=phone_number, amount=amount, reference_code=account,
                                      callback_url="https://lipafair.herokuapp.com/api/stk-checkout-callback/")
        response = dict(stk_request.initiate_txn())

        if response.get('ResponseCode') == '0':
            txn = MpesaTransaction.objects.create(
                user_id=user_id,
                txn_id=response.get('CheckoutRequestID'),
                reason="Direct checkout",
                amount=Decimal(amount),
                account=account,
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
        return MpesaTransaction.objects.filter(user_id=self.kwargs.get('user_id', '')).order_by('txn_date')



class AllTransactionsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id', '')

        mpesa_txns = MpesaTransaction.objects.filter(user_id=user_id,status='success')
        wallet_txns = WalletTransaction.objects.filter(user_id=user_id, status='success')
        print(mpesa_txns)
        print(wallet_txns)
        data = []
        for txn in mpesa_txns:
            data.append(
                {
                    "user_id": txn.user_id,
                    "txn_id": txn.mpesa_receipt,
                    "amount": txn.amount,
                    "account": txn.account,
                    "txn_type": txn.txn_type,
                    "status": txn.status,
                    "txn_date": txn.txn_date.strftime("%d/%m/%Y %H:%M:%S")


                }
            )

        for txn in wallet_txns:
            data.append(
                {
                    "user_id": txn.user_id,
                    "txn_id": txn.txn_id,
                    "amount": txn.amount,
                    "account": txn.account,
                    "txn_type": txn.txn_type,
                    "status": txn.status,
                    "txn_date": txn.txn_date.strftime("%d/%m/%Y %H:%M:%S")

                }
            )

        return Response(data=data, status=status.HTTP_200_OK)



class B2CTransactionListView(generics.ListAPIView):
    serializer_class = B2CTransactionSerializer

    def get_queryset(self):
        account = self.kwargs.get('account', '')
        return B2CWithdrawalRequest.objects.filter(account_no=account)

class CheckoutFromWalletAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_wallet_id = data.get('client_wallet_id')
        store_account_no = data.get('account_no')
        amount = data.get('amount')

        try:
            client_wallet = Wallet.objects.get(wallet_id=client_wallet_id)
            #check the available balance now

            balance = int(client_wallet.current_balance)
            if balance >= int(amount):
                # complete transaction since the funds are available
                txn = WalletTransaction.objects.create(
                    user_id=data.get('user_id'),
                    txn_id=uuid.uuid4().hex.upper(),
                    amount=amount,
                    account=store_account_no,
                    status="success"
                )
                txn.save()
                checkout_from_wallet_completed.send(sender=self.__class__, client_wallet=client_wallet, transaction=txn)
                return Response(status=status.HTTP_200_OK, data={
                    'message': "Checkout completed successfully"
                })
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    'message': f"You do not have sufficient funds to complete the transaction. Your current balance is Ksh {client_wallet.current_balance}"
                })

        except Wallet.DoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                'message': "Could not find a matching client wallet."
            })




class WithdrawFromWallet(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        store_wallet_id = data.get('store_wallet_id', '')

        amount = int(data.get('amount', 0))

        #get the store
        manager = StoreWalletManager()
        tariff_manager = B2CTariffManager()
        charges = tariff_manager.get_charges(amount=amount)
        if charges is not None:
            wallet_data = dict(manager.get_wallet(account_no=store_wallet_id))
            if wallet_data.get('status') == status.HTTP_200_OK:
                available_balance = int(wallet_data.get('amount',  0))
                net_amount = amount + charges
                if available_balance >=net_amount:
                    #funds available for withdrawal

                    b2c_api = B2C(env=settings.MPESA_ENV)
                    phone_number = settings.MPESA_B2C_TEST_MSISDN if settings.MPESA_ENV == 'sandbox' else data.get('phone_number')

                    result = dict(b2c_api.initiate_b2c(phone_number=phone_number, amount=data.get('amount'),occasion=data.get('occasion')))

                    print(result)
                    if result.__contains__("ResponseCode"):

                        if result.get('ResponseCode').strip() == '0':
                            withdrawal_request = B2CWithdrawalRequest.objects.create(
                                account_no=data.get('store_wallet_id'),
                                txn_id=result.get('ConversationID'),
                                txn_ref="",
                                amount=data.get('amount'),
                                phone_number=phone_number,
                                customer_name=""
                            )
                            withdrawal_request.save()
                            return Response(status=status.HTTP_200_OK,
                                            data={'message': "Request submitted successfully for processing"})
                        else:
                            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                                'message': "Error occurred while processing your request try again later."
                            })
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={
                            'message': "Unable to get response from b2c api."
                        })

                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={
                        'message': "You do not have sufficient balance."
                    })
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    'message': "Unable to get matching wallet details."
                })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Failed to calculate withdrawal charges. Please try again later."
            })



class WalletWithdrawalCallback(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        callback_result = data.get('Result')
        print(callback_result)

        if str(callback_result.get('ResultCode')) == '0':
            txn_id = callback_result.get('ConversationID')
            try:
                txn = B2CWithdrawalRequest.objects.get(txn_id=txn_id, status='pending')
                if txn:
                    if txn.status == 'pending':
                        #send a signal to update the wallet signal should be sent once. that is why we send it before switching from pending to success status
                        b2c_payment_completed.send(sender=self.__class__, transaction=txn)

                    txn.status = 'success'
                    txn.txn_ref = str(callback_result.get('TransactionID'))
                    txn.customer_name = callback_result.get('ResultParameters').get('ResultParameter')[4].get('Value')

                    txn.save()

                    return Response(status=status.HTTP_200_OK, data={"message": "Funds transferred successfully."})
            except B2CWithdrawalRequest.DoesNotExist as e:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"message": "Error occurred while transferring funds please try again later"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"message": "Unable to complete your request for now."})



