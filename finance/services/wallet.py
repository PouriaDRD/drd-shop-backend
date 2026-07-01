import logging

from django.db import transaction
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
    @transaction.atomic
    def deposit(
        wallet_id,
        amount: int,
    ) -> WalletModel:
        """
        Increase wallet balance.

        Args:
            wallet_id:
                Wallet identifier.

            amount:
                Positive amount.

        Returns:
            Updated wallet.
        """

        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        wallet = WalletRepository.lock(wallet_id)

        wallet.balance += amount

        WalletRepository.update_balance(
            wallet,
            wallet.balance,
        )

        logger.info(
            f"Wallet credited | wallet={wallet.id} amount={amount} balance={wallet.balance}",
        )

        return wallet

    @staticmethod
    @transaction.atomic
    def withdraw(
        wallet_id,
        amount: int,
    ) -> WalletModel:
        """
        Decrease wallet balance.

        Raises:
            ValidationError:
                If balance is insufficient.
        """

        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        wallet = WalletRepository.lock(wallet_id)

        if wallet.balance < amount:
            raise ValidationError("Insufficient wallet balance.")

        wallet.balance -= amount

        WalletRepository.update_balance(
            wallet,
            wallet.balance,
        )

        logger.info(
            f"Wallet debited | wallet={wallet.id} amount={amount} balance={wallet.balance}"
        )

        return wallet

    @staticmethod
    @transaction.atomic
    def set_balance(
        wallet_id,
        balance: int,
    ) -> WalletModel:
        """
        Force wallet balance.

        Intended for internal use only.
        """

        wallet = WalletRepository.lock(wallet_id)

        WalletRepository.update_balance(
            wallet,
            balance,
        )

        logger.warning(
            f"Wallet balance manually changed | wallet={wallet.id} balance={balance}"
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
