from django.urls import path

from .views import OTPRequestAPIView, OTPVerifyAPIView, TokenRefreshAPIView

urlpatterns = [
    path("request-otp/", OTPRequestAPIView.as_view(), name="otp-request"),
    path("verify-otp/", OTPVerifyAPIView.as_view(), name="otp-verify"),
    path("refresh/", TokenRefreshAPIView.as_view(), name="refresh-token"),
]
