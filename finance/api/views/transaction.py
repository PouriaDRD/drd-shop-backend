import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from finance.models import TransactionModel
from finance.repositories import TransactionRepository
from finance.api.serializers import TransactionSerializer

logger = logging.getLogger("finance.transaction-list")


class TransactionListAPIView(ListAPIView):
    """
    List authenticated user's wallet transactions.
    """

    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]

    serializer_class = TransactionSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore
        """
        Return transactions of user's wallet.
        """

        wallet = getattr(self.request.user, "wallet", None)

        if wallet is None:
            return TransactionModel.objects.none()

        return TransactionRepository.get_wallet_transactions(wallet.id)

    def list(self, request: Request, *args, **kwargs):
        """
        Return transactions in standardized API response.
        """

        try:
            user = request.user

            queryset = self.get_queryset()

            serializer = self.get_serializer(queryset, many=True)

            logger.info(f"Transactions retrieved for user: {user}")

            return APIResponse.success(
                data=serializer.data,
                message="تراکنش های کیف پول با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error while retrieving transactions: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در دریافت تراکنش های کیف پول.",
            )
