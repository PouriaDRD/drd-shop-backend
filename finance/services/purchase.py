from rest_framework.exceptions import ValidationError
from finance.models import WalletModel
from finance.enums import TransactionType, TransactionStatus, PaymentMethod
from finance.repositories import (
    TransactionRepository,
    LedgerRepository,
    WalletRepository,
)


class PurchaseService:
    """Purchase service."""

    @staticmethod
    def purchase(
        amount: int,
        wallet: WalletModel,
        method: PaymentMethod = PaymentMethod.CARD_TO_CARD,
        **kwargs,
    ):
        """
        Deduct money from wallet.
        """

        balance = WalletRepository.get_balance(wallet=wallet)

        if balance < amount:
            raise ValidationError("Insufficient balance.")

        transaction = TransactionRepository.create(
            amount=amount,
            wallet=wallet,
            method=method,
            type=TransactionType.PURCHASE,
            status=TransactionStatus.COMPLETED,
            **kwargs,
        )

        LedgerRepository.create(
            amount=-amount,
            wallet=wallet,
            transaction=transaction,
        )

        return transaction
