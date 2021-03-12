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
]