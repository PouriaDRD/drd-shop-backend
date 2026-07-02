import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import CreateAPIView, ListAPIView

from config.utils import APIResponse
from finance.repositories import DepositRepository
from finance.api.serializers import DepositCreateSerializer, DepositRetrieveSerializer

logger = logging.getLogger("finance.deposit")


class DepositCreateAPIView(CreateAPIView):
    """
    Create a deposit request.
    """

    http_method_names = ["post"]

    serializer_class = DepositCreateSerializer

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            user = request.user
            serializer = self.get_serializer(
                data=request.data,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)

            result = serializer.save()

            serialized_data = DepositRetrieveSerializer(result).data

            logger.info(
                f"Deposit Request Created successfully: user={user} deposit={result}"
            )

            return APIResponse.success(
                data=serialized_data,
                message="درخواست واریز با موفقیت ایجاد شد.",
                status_code=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            logger.warning(f"Error Creating Deposit Request: {e.get_codes()}")
            return APIResponse.error(
                message=f"خطا در ایجاد درخواست واریز",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Error Creating Deposit Request: {e}")
            return APIResponse.error(
                message=f"خطا در ایجاد درخواست واریز",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DepositListAPIView(ListAPIView):
    """
    Retrieve authenticated user's deposit requests.
    """

    http_method_names = ["get"]

    serializer_class = DepositRetrieveSerializer

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore
        """
        Return authenticated user's deposit requests.
        """

        return DepositRepository.get_wallet_deposits(
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
                f"Deposit list retrieved | user={request.user} | count={len(serializer.data)}"
            )

            return APIResponse.success(
                data=serializer.data,
                message="درخواست های واریز با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )

        except ValidationError as exc:
            logger.warning(
                f"Failed to retrieve deposit requests | user={request.user} | errors={exc.get_codes()}"
            )

            return APIResponse.error(
                message="خطا در دریافت درخواست های واریز.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.exception(
                f"Unexpected error while retrieving deposit requests | user={request.user} | errors={e}"
            )

            return APIResponse.error(
                message="خطا در دریافت درخواست های واریز.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
