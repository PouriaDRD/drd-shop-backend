from django.db import transaction
from django.db.models import QuerySet

from accounts.models import UserModel
from finance.models import WalletModel


class WalletRepository:
    """
    Repository layer for wallet persistence.

    This layer is responsible only for database operations.
    """

    @staticmethod
    @transaction.atomic
    def create(user: UserModel) -> WalletModel:
        """
        Create a wallet for a user.

        Args:
            user: Wallet owner.

        Returns:
            Newly created wallet.
        """

        return WalletModel.objects.create(user=user)

    @staticmethod
    def get_by_id(wallet_id) -> WalletModel | None:
        """
        Retrieve wallet by id.
        """

        return WalletModel.objects.select_related("user").filter(id=wallet_id).first()

    @staticmethod
    def get_by_user(user: UserModel) -> WalletModel | None:
        """
        Retrieve wallet by user.
        """

        return WalletModel.objects.select_related("user").filter(user=user).first()

    @staticmethod
    def get_all() -> QuerySet[WalletModel]:
        """
        Retrieve all wallets.
        """

        return WalletModel.objects.select_related("user").all()

    @staticmethod
    def exists(user: UserModel) -> bool:
        """
        Check whether user already owns a wallet.
        """

        return WalletModel.objects.filter(user=user).exists()

    @staticmethod
    @transaction.atomic
    def lock(wallet_id) -> WalletModel:
        """
        Lock wallet row.

        Notes:
            Must be called inside an atomic transaction.
        """

        return (
            WalletModel.objects.select_for_update()
            .select_related("user")
            .get(id=wallet_id)
        )
