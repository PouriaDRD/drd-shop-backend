from django.urls import path


from .views import (
    LoginAPIView,
    RegisterAPIView,
    TokenRefreshAPIView,
    SendLoginOTPAPIView,
    VerifyLoginOTPAPIView,
    MyLoginHistoryAPIView,
)

urlpatterns = [
    # Login history
    path("login-history/", MyLoginHistoryAPIView.as_view(), name="login-history"),
    # Normal login
    path("login/", LoginAPIView.as_view(), name="login"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    # OTP login
    path("request-otp/", SendLoginOTPAPIView.as_view(), name="request-otp"),
    path("verify-otp/", VerifyLoginOTPAPIView.as_view(), name="verify-otp"),
    # Refresh token
    path("refresh/", TokenRefreshAPIView.as_view(), name="refresh-token"),
]
