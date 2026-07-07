from django.urls import path

from finance.api.views import (
    CardListAPIView,
    DepositListAPIView,
    PurchaseListAPIView,
    DepositCreateAPIView,
    WalletRetrieveAPIView,
    TransactionListAPIView,
    RefundToUserListAPIView,
    RefundToWalletListAPIView,
    PurchaseStatisticsAPIView,
)

urlpatterns = [
    path(
        "purchase-statistics/",
        PurchaseStatisticsAPIView.as_view(),
        name="purchase-statistics",
    ),
    path("cards/", CardListAPIView.as_view(), name="cards"),
    path("my-wallet/", WalletRetrieveAPIView.as_view(), name="my-wallet"),
    path("my-deposits/", DepositListAPIView.as_view(), name="my-deposits"),
    path("request-deposit/", DepositCreateAPIView.as_view(), name="request-deposit"),
    path("my-transactions/", TransactionListAPIView.as_view(), name="my-transactions"),
    path("my-purchases/", PurchaseListAPIView.as_view(), name="my-purchases"),
    path(
        "my-refund-to-wallet/",
        RefundToWalletListAPIView.as_view(),
        name="my-refund-to-wallet",
    ),
    path(
        "my-refund-to-user/",
        RefundToUserListAPIView.as_view(),
        name="my-refund-to-user",
    ),
]
