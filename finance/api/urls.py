from django.urls import path

from .views import TransactionListAPIView, WalletRetrieveAPIView

urlpatterns = [
    path("my-wallet/", WalletRetrieveAPIView.as_view(), name="my-wallet"),
    path(
        "my-transactions/", TransactionListAPIView.as_view(), name="my-transaction-list"
    ),
]
