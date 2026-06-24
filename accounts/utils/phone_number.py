import re
from django.core.exceptions import ValidationError

# Mapping Persian digits to English digits
PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

# Mapping Arabic digits to English digits
ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def normalize_digits(value: str):
    """
    Convert Persian and Arabic digits to English digits.
    """
    return value.translate(PERSIAN_DIGITS).translate(ARABIC_DIGITS)


def normalize_iranian_mobile(value: str):
    """
    Normalize Iranian mobile number:
    - remove spaces
    - convert Persian/Arabic digits to English
    - convert +98 / 0098 to 09 format
    """

    if value is None:
        return None

    value = value.strip().replace(" ", "")
    value = normalize_digits(value)

    # Convert international format to local format
    if value.startswith("+98"):
        value = "0" + value[3:]

    if value.startswith("0098"):
        value = "0" + value[4:]

    return str(value)


def validate_iranian_mobile(value: str):
    """
    Validate Iranian mobile number format: 09xxxxxxxxx
    Raises ValidationError if invalid.
    """

    value = normalize_digits(value)

    pattern = r"^09\d{9}$"

    if not re.match(pattern, value):
        raise ValidationError(
            "Please enter a valid phone number (09xxxxxxxxx).",
        )
