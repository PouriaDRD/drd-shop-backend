from django.urls import path

from .views.product import ProductListAPIView, ProductDetailAPIView


from .views.coupon import (
    ApplyCouponAPIView,
    RemoveCouponAPIView,
)

from .views.provisions import V2rayVPNListAPIView

urlpatterns = [
    # VPN Services
    path(
        "my-v2ray-vpn-services/",
        V2rayVPNListAPIView.as_view(),
        name="v2ray-vpn-service-list",
    ),
    # Products
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path(
        "products/<uuid:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    # Coupons
    path("my-cart/apply-coupon/", ApplyCouponAPIView.as_view()),
    path("my-cart/remove-coupon/", RemoveCouponAPIView.as_view()),
]
