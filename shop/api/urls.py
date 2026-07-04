from django.urls import path

from shop.api.views.product import ProductListAPIView, ProductDetailAPIView
from shop.api.views.cart import (
    CartAPIView,
    AddCartItemAPIView,
    UpdateCartItemAPIView,
    DeleteCartItemAPIView,
)
from shop.api.views.coupon import (
    ApplyCouponAPIView,
    RemoveCouponAPIView,
)

urlpatterns = [
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
    # Coupons
    path("my-cart/apply-coupon/", ApplyCouponAPIView.as_view()),
    path("my-cart/remove-coupon/", RemoveCouponAPIView.as_view()),
]
