from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from finance.services import DepositService
from finance.models import DepositRequestModel
from finance.enums import DepositPaymentMethod

MAX_RECEIPT_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_receipt_size(image):
    if image.size > MAX_RECEIPT_SIZE:
        raise ValidationError("حجم تصویر رسید نباید بیشتر از ۵ مگابایت باشد.")

    return image


ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
]


def validate_receipt_file_type(image):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError("فرمت تصویر باید JPG، PNG یا WEBP باشد.")

    return image


class DepositCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a deposit request.
    """

    amount = serializers.IntegerField(
        required=True,
        min_value=10_000,
        error_messages={
            "required": "Amount is required.",
            "invalid": "Amount must be a valid number.",
            "min_value": "Amount must be at least 10,000.",
        },
    )

    payment_method = serializers.ChoiceField(
        choices=DepositPaymentMethod.choices,
        required=True,
        error_messages={
            "required": "Payment method is required.",
            "invalid_choice": "Invalid payment method.",
        },
    )

    reference_number = serializers.CharField(
        required=False,
        max_length=255,
        trim_whitespace=True,
        # error_messages={
        #     "required": "Reference number is required.",
        #     "blank": "Reference number is required.",
        # },
    )

    tracking_code = serializers.CharField(
        required=False,
        max_length=255,
        trim_whitespace=True,
        # error_messages={
        #     "required": "Tracking code is required.",
        #     "blank": "Tracking code is required.",
        # },
    )

    sender_name = serializers.CharField(
        required=True,
        max_length=255,
        trim_whitespace=True,
        error_messages={
            "required": "Sender name is required.",
            "blank": "Sender name is required.",
        },
    )

    sender_card_number = serializers.CharField(
        required=True,
        min_length=16,
        max_length=16,
        trim_whitespace=True,
        error_messages={
            "required": "Sender card number is required.",
            "blank": "Sender card number is required.",
            "min_length": "Sender card number must be at least 16 digits.",
            "max_length": "Sender card number must be at most 16 digits.",
        },
    )

    transaction_date = serializers.DateField(
        required=True,
        error_messages={
            "required": "Transaction date is required.",
        },
    )

    transaction_time = serializers.TimeField(
        required=True,
        error_messages={
            "required": "Transaction time is required.",
        },
    )

    receipt_image = serializers.ImageField(
        required=True,
        validators=[
            validate_receipt_size,
            validate_receipt_file_type,
        ],
        error_messages={
            "required": "Receipt image is required.",
            "invalid_image": "Uploaded file must be a valid image.",
        },
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
    )

    class Meta:
        model = DepositRequestModel
        fields = (
            "amount",
            "payment_method",
            "reference_number",
            "tracking_code",
            "sender_name",
            "sender_card_number",
            "transaction_date",
            "transaction_time",
            "receipt_image",
            "note",
        )

    def validate_sender_name(self, value: str | None) -> str | None:
        if value:
            value = " ".join(value.strip().split())

        return value

    def validate_sender_card_number(self, value: str | None) -> str | None:
        if not value:
            return value

        return value.replace("-", "").replace(" ", "").strip()

    def validate_reference_number(self, value: str | None) -> str | None:
        if value:
            value = value.strip()

        return value

    def validate_tracking_code(self, value: str | None) -> str | None:
        if value:
            value = value.strip()

        return value

    def validate(self, attrs: dict) -> dict:
        """
        Cross-field validation.
        """

        payment_method = attrs.get("payment_method")
        receipt_image = attrs.get("receipt_image")

        if (
            payment_method == DepositPaymentMethod.CARD_TO_CARD
            and receipt_image is None
        ):
            raise serializers.ValidationError(
                {
                    "receipt_image": [
                        "Receipt image is required for card-to-card deposits."
                    ]
                }
            )

        return attrs

    def create(self, validated_data: dict):
        """
        Delegate creation to the service layer.
        """
        request = self.context.get("request")
        user = self.context["request"].user

        if not request or not hasattr(user, "wallet"):
            raise serializers.ValidationError({"wallet": "User wallet not found."})

        wallet = user.wallet

        result = DepositService.create(wallet, **validated_data)

        return result


class DepositRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying deposit requests.
    """

    class Meta:
        model = DepositRequestModel
        fields = (
            "id",
            "amount",
            "payment_method",
            "reference_number",
            "tracking_code",
            "sender_name",
            "sender_card_number",
            "transaction_date",
            "transaction_time",
            "note",
            "status",
            "is_processed",
            "created_at",
        )
        read_only_fields = ["__all__"]
