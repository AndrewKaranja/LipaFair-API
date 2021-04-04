from django.urls import path
from api import views

urlpatterns = [
    path('wallets/', views.WalletListCreatePIView.as_view()),
    path('wallets/<user_id>/', views.WalletDetailView.as_view()),
    path('wallet-topup/', views.TopUpWalletRequest.as_view()),
    path('wallettopup-callback/', views.TopUpWalletCallback.as_view()),
    path('stk-checkout/', views.DirectSTKCheckoutRequest.as_view()),
    path('stk-checkout-callback/', views.DirectCheckoutSTKCallback.as_view()),
    path('mpesa-transactions/<user_id>/', views.TransactionsListAPIView.as_view()),
    path('all-transactions/<user_id>/', views.AllTransactionsListAPIView.as_view()),
    path('b2c-transactions/<account>/', views.B2CTransactionListView.as_view()),
    path('wallet-checkout/', views.CheckoutFromWalletAPIView.as_view()),
    path('withdraw-from-wallet/', views.WithdrawFromWallet.as_view()),
    path('withdraw-from-wallet-callback/', views.WalletWithdrawalCallback.as_view()),
    path('coupons/', views.CouponsListCreateView.as_view()),
    path('coupons/<coupon_id>/', views.CouponDetailView.as_view()),
]