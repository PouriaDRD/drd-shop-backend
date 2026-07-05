from django.urls import path

from shop.api.views.product import ProductListAPIView, ProductDetailAPIView
from shop.api.views.cart import (
    CartAPIView,
    AddCartItemAPIView,
    UpdateCartItemAPIView,
    DeleteCartItemAPIView,
    CheckoutCreateAPIView,
)

from shop.api.views.order import OrderListAPIView

from shop.api.views.coupon import (
    ApplyCouponAPIView,
    RemoveCouponAPIView,
)

from shop.api.views.vpn_service import VPNServiceListAPIView

urlpatterns = [
    # Orders
    path("my-orders/", OrderListAPIView.as_view(), name="order-list"),
    # VPN Services
    path("my-vpn-services/", VPNServiceListAPIView.as_view(), name="vpn-service-list"),
    # Products
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path(
        "products/<uuid:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    # Cart
    path("my-cart/", CartAPIView.as_view(), name="my-cart"),
    path("my-cart/add-item/", AddCartItemAPIView.as_view(), name="add-cart-item"),
    path(
        "my-cart/update-item/<uuid:item_id>/",
        UpdateCartItemAPIView.as_view(),
        name="update-cart-item",
    ),
    path(
        "my-cart/remove-item/<uuid:item_id>/",
        DeleteCartItemAPIView.as_view(),
        name="delete-cart-item",
    ),
    path("checkout/", CheckoutCreateAPIView.as_view(), name="checkout"),
    # Coupons
    path("my-cart/apply-coupon/", ApplyCouponAPIView.as_view()),
    path("my-cart/remove-coupon/", RemoveCouponAPIView.as_view()),
]
