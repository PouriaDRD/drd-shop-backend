from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from finance.models import WalletModel
from finance.api.serializers import WalletSerializer


class WalletRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve authenticated user's wallet.

    Methods:
        GET

    Permissions:
        - Authenticated users only
    """

    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    serializer_class = WalletSerializer

    def get_object(self) -> WalletModel:  # type: ignore
        """
        Return current authenticated user's wallet.
        """

        user = self.request.user
        wallet = getattr(user, "wallet", None)

        return wallet  # type: ignore
