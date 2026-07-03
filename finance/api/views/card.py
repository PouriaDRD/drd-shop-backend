import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from finance.models import CardModel
from finance.api.serializers import CardSerializer

logger = logging.getLogger("finance.card-list")


class CardListAPIView(ListAPIView):
    http_method_names = ["get"]

    serializer_class = CardSerializer

    queryset = CardModel.objects.all()
    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request: Request, *args, **kwargs):
        """
        Return card available for user.
        """

        try:
            user = request.user

            queryset = self.get_queryset()

            serializer = self.get_serializer(queryset, many=True)

            logger.info(f"Card retrieved for user: {user}")

            return APIResponse.success(
                data=serializer.data,
                message="اطلاعات کارت با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error while retrieving card: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در دریافت کارت کیف پول.",
            )
