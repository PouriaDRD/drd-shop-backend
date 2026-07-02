from django.urls import path

from finance.api.views import (
    DepositCreateAPIView,
    DepositListAPIView,
    TransactionListAPIView,
    WalletRetrieveAPIView,
)

urlpatterns = [
    path("my-deposits/", DepositListAPIView.as_view(), name="my-deposits"),
    path("request-deposit/", DepositCreateAPIView.as_view(), name="request-deposit"),
    path("my-wallet/", WalletRetrieveAPIView.as_view(), name="my-wallet"),
    path("my-transactions/", TransactionListAPIView.as_view(), name="my-transactions"),
]
