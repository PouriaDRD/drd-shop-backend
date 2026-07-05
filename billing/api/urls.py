from django.urls import path

from .views.cart import (
    CartAPIView,
    AddCartItemAPIView,
    UpdateCartItemAPIView,
    DeleteCartItemAPIView,
    CheckoutCreateAPIView,
)

from .views.order import OrderListAPIView

urlpatterns = [
    # Orders
    path("my-orders/", OrderListAPIView.as_view(), name="order-list"),
    path("checkout/", CheckoutCreateAPIView.as_view(), name="checkout"),
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
]
