import logging
from rest_framework.exceptions import ValidationError

from accounts.models import UserModel

from finance.models import WalletModel
from finance.repositories import WalletRepository

logger = logging.getLogger("finance")


class WalletService:
    """
    Business layer for wallet operations.

    Responsible for:
        - Wallet creation
        - Balance updates
        - Safe debit / credit operations
        - Preventing race conditions
    """

    @staticmethod
    def create(user: UserModel) -> WalletModel:
        """
        Create a wallet for a user.

        Raises:
            ValidationError:
                If the wallet already exists.
        """

        if WalletRepository.exists(user):
            raise ValidationError("Wallet already exists.")

        wallet = WalletRepository.create(user)

        logger.info(
            f"Wallet created | wallet={wallet.id} user={user.id}",
        )

        return wallet

    @staticmethod
    def get_balance(wallet: WalletModel) -> int:
        """
        Return current wallet balance.
        """

        return wallet.balance

    @staticmethod
    def has_balance(
        wallet: WalletModel,
        amount: int,
    ) -> bool:
        """
        Check whether wallet has enough balance.
        """

        return wallet.balance >= amount
