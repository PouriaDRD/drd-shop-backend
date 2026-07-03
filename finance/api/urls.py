from django.urls import path

from finance.api.views import (
    CardListAPIView,
    DepositCreateAPIView,
    DepositListAPIView,
    TransactionListAPIView,
    WalletRetrieveAPIView,
)

urlpatterns = [
    path("cards/", CardListAPIView.as_view(), name="cards"),
    path("my-deposits/", DepositListAPIView.as_view(), name="my-deposits"),
    path("request-deposit/", DepositCreateAPIView.as_view(), name="request-deposit"),
    path("my-wallet/", WalletRetrieveAPIView.as_view(), name="my-wallet"),
    path("my-transactions/", TransactionListAPIView.as_view(), name="my-transactions"),
]
