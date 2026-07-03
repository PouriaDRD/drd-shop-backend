import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from finance.repositories import RefundRepository
from finance.api.serializers import RefundToUserRetrieveSerializer

logger = logging.getLogger("finance.refund-to-user-list")


class RefundToUserListAPIView(ListAPIView):
    """
    Retrieve authenticated user's refund to user requests.
    """

    http_method_names = ["get"]

    serializer_class = RefundToUserRetrieveSerializer

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore
        """
        Return authenticated user's deposit requests.
        """

        return RefundRepository.get_wallet_refunds_to_user(
            wallet_id=self.request.user.wallet.id,  # type: ignore
        )

    def get(self, request: Request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            serializer = self.get_serializer(
                queryset,
                many=True,
            )

            logger.info(
                f"Refund to user list retrieved | user={request.user} | count={len(serializer.data)}"
            )

            return APIResponse.success(
                data=serializer.data,
                message="درخواست های استرداد به کاربر با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )

        except ValidationError as exc:
            logger.warning(
                f"Failed to retrieve Refund to user  requests | user={request.user} | errors={exc.get_codes()}"
            )

            return APIResponse.error(
                message="خطا در دریافت درخواست های استرداد به کاربر.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.exception(
                f"Unexpected error while retrieving Refund to user requests | user={request.user} | errors={e}"
            )

            return APIResponse.error(
                message="خطا در دریافت درخواست های استرداد به کاربر.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
