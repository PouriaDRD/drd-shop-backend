import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse

from commerce.models import CouponModel
from commerce.api.serializers import ApplyCouponSerializer

from billing.services.cart import CartService
from billing.api.serializers import CartSerializer

logger = logging.getLogger("commerce.coupon")


class ApplyCouponAPIView(CreateAPIView):
    """
    Apply a coupon to the user's cart.
    """

    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    serializer_class = ApplyCouponSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            code = serializer.validated_data["code"]
            coupon = CouponModel.objects.filter(
                code=code,
                is_active=True,
            ).first()
            cart = CartService.get_or_create_cart(request.user)

            cart.coupon = coupon
            cart.save()

            CartService.recalculate(cart)

            logger.info(f"Coupon applied: {coupon.code}, wallet: {cart.user.email}")
            return APIResponse.success(
                data=CartSerializer(cart).data,
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error while applying coupon: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در افزودن کوپن.",
            )


class RemoveCouponAPIView(APIView):
    """
    Remove a coupon from the user's cart.
    """

    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            cart = CartService.get_or_create_cart(request.user)

            cart.coupon = None
            cart.save()

            CartService.recalculate(cart)

            logger.info(f"Coupon removed: {cart.user.email}")
            return APIResponse.success(
                data=CartSerializer(cart).data,
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error while removing coupon: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در حذف کوپن.",
            )
