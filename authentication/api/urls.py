from django.urls import path


from .views import (
    LoginAPIView,
    RegisterAPIView,
    TokenRefreshAPIView,
    SendLoginOTPAPIView,
    VerifyLoginOTPAPIView,
)

urlpatterns = [
    # Normal login
    path("login/", LoginAPIView.as_view(), name="login"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    # OTP login
    path("otp/send/", SendLoginOTPAPIView.as_view(), name="otp-send"),
    path("otp/verify/", VerifyLoginOTPAPIView.as_view(), name="otp-verify"),
    # Refresh token
    path("refresh/", TokenRefreshAPIView.as_view(), name="refresh-token"),
]
