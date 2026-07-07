import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from finance.services import PurchaseService
from finance.api.serializers import PurchaseStatisticsSerializer

logger = logging.getLogger("finance.purchase-statistics")


class PurchaseStatisticsAPIView(RetrieveAPIView):
    """
    Return user purchase statistics.
    """

    http_method_names = ["get"]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    serializer_class = PurchaseStatisticsSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request: Request, *args, **kwargs):

        try:
            wallet_id = request.user.wallet.id
            result = PurchaseService.get_purchase_statistics(wallet_id)

            logger.info(
                f"User purchase statistics retrieved: {wallet_id}, user={str(request.user)}"
            )
            return APIResponse.success(
                data=result,
                message="داده های کیف پول با موفیقت دریافت شد!",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error getting user purchase statistics: {e}")
            return APIResponse.error(
                message="خطا در دریافت داده های کیف پول رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
