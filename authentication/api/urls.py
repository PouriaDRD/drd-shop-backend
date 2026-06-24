from django.urls import path

from .views import OTPRequestAPIView, OTPVerifyAPIView

urlpatterns = [
    path("request-otp/", OTPRequestAPIView.as_view(), name="otp-request"),
    path("verify-otp/", OTPVerifyAPIView.as_view(), name="otp-verify"),
]
