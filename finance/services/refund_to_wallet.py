import logging

from django.db import transaction
from rest_framework.exceptions import ValidationError

from finance.enums import (
    TransactionType,
    TransactionStatus,
)

from finance.repositories import (
    WalletRepository,
    TransactionRepository,
    LedgerRepository,
)

logger = logging.getLogger("finance.refund_service")


class RefundService:
    """
    Handles refund flows:

    1. REFUND_TO_WALLET → money goes back to user wallet
    2. REFUND_TO_USER → money sent outside system (cash/bank)
    """

    # --------------------------------------------------------
    # REFUND TO WALLET
    # --------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def refund_to_wallet(wallet_id: str, amount: int, description: str = ""):
        """
        Refund money back into user's wallet.
        """

        wallet = WalletRepository.lock(wallet_id)

        if amount <= 0:
            raise ValidationError("Invalid refund amount.")

        balance_before = wallet.balance
        balance_after = balance_before + amount

        transaction_obj = TransactionRepository.create(
            wallet=wallet,
            amount=amount,
            transaction_type=TransactionType.REFUND_TO_WALLET,
            status=TransactionStatus.APPROVED,
            description=description or "Refund to wallet",
        )

        LedgerRepository.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.REFUND_TO_WALLET,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

        logger.info(
            f"REFUND_TO_WALLET completed | wallet={wallet_id} amount={amount}",
        )

        return transaction_obj

    # --------------------------------------------------------
    # REFUND TO USER (external payout)
    # --------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def refund_to_user(wallet_id: str, amount: int, description: str = ""):
        """
        Refund money outside system (bank/card/cash).
        """

        wallet = WalletRepository.lock(wallet_id)

        if amount <= 0:
            raise ValidationError("Invalid refund amount.")

        if wallet.balance < amount:
            raise ValidationError("Insufficient wallet balance.")

        balance_before = wallet.balance
        balance_after = balance_before - amount

        transaction_obj = TransactionRepository.create(
            wallet=wallet,
            amount=-amount,
            transaction_type=TransactionType.REFUND_TO_USER,
            status=TransactionStatus.APPROVED,
            description=description or "Refund to user",
        )

        LedgerRepository.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.REFUND_TO_USER,
            amount=-amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

        logger.info(
            f"REFUND_TO_USER completed | wallet={wallet_id} amount={amount}",
        )

        return transaction_obj
