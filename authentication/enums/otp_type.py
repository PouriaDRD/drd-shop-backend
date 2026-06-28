from django.db import models


class OTPType(models.TextChoices):
    LOGIN = "login", "Login"
    REGISTER = "register", "Register"
    VERIFY_EMAIL = "verify_email", "Verify email"
    RESET_PASSWORD = "reset_password", "Reset password"
