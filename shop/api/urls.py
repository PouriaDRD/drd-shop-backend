from django.urls import path

from shop.api.views import ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path(
        "products/<uuid:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
]
