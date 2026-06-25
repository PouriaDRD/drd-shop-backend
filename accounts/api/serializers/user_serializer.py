from accounts.models import UserModel
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for UserModel.
    """

    class Meta:
        model = UserModel
        fields = (
            "id",
            "phone_number",
            "email",
            "role",
            "status",
            "last_login",
            "created_at",
        )
        read_only_fields = ["__all__"]
