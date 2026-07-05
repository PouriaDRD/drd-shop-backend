import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from billing.services import CartService
from billing.api.serializers import CartSerializer

logger = logging.getLogger("billing.cart")


class CartAPIView(RetrieveAPIView):
    """
    Retrieve the user's cart.
    """

    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    serializer_class = CartSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request: Request, *args, **kwargs):
        try:
            cart = CartService.get_or_create_cart(request.user)
            serializer = self.get_serializer(cart)

            logger.info(f"Cart retrieved: {cart.id}, user: {cart.user.email}")

            return APIResponse.success(
                data=serializer.data,
                message="سبر خرید با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error while retrieving cart: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در دریافت سبد خرید.",
            )
