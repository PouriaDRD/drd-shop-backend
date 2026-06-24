import uuid
from django.db import models
from django.utils import timezone
from accounts.utils import validate_iranian_mobile, normalize_iranian_mobile


class OTPModel(models.Model):
    """
    OTP storage model.

    Security features:
    - expiration time
    - attempt tracking
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_number = models.CharField(
        max_length=11,
        validators=[validate_iranian_mobile],
    )

    code = models.CharField(max_length=6)

    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otp_codes"
        ordering = ["-created_at"]

        verbose_name = "OTP Code"
        verbose_name_plural = "OTP Codes"

    def __str__(self):
        return f"{self.phone_number} | {self.code}"

    def save(self, *args, **kwargs):
        self.phone_number = normalize_iranian_mobile(self.phone_number)
        super().save(*args, **kwargs)

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at
