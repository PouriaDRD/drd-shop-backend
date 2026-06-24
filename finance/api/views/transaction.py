from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from finance.models import TransactionModel
from finance.repositories import TransactionRepository
from finance.api.serializers import TransactionSerializer


class TransactionListAPIView(ListAPIView):
    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]

    serializer_class = TransactionSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore
        """
        Return authenticated user's wallet transactions.
        """

        user = self.request.user
        wallet = getattr(user, "wallet", None)

        if wallet is None:
            return TransactionModel.objects.none()

        qs = TransactionRepository.get_wallet_transactions(wallet.id)
        return qs
