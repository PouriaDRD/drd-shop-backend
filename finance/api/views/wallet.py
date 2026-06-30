import logging
from rest_framework.request import Request
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from finance.models import WalletModel
from finance.api.serializers import WalletSerializer

logger = logging.getLogger("finance.wallet")


class WalletRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve authenticated user's wallet.
    """

    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    serializer_class = WalletSerializer

    def get_object(self) -> WalletModel:  # type: ignore
        """
        Return wallet of authenticated user.
        """

        wallet = getattr(self.request.user, "wallet", None)

        return wallet  # type: ignore

    def get(self, request: Request, *args, **kwargs):
        """
        Return wallet data in standardized API response.
        """
        user = request.user
        user_id = str(user.id)

        wallet = self.get_object()
        serializer = self.get_serializer(wallet)

        logger.info(
            "Wallet retrieved for user %s",
            f"{user_id[:4]}*****{user_id[-2:]}",
        )

        return APIResponse.success(
            data=serializer.data,
            message="کیف پول با موفقیت دریافت شد.",
        )
