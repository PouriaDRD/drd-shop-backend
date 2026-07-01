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
    RefundRepository,
)

logger = logging.getLogger("finance.refund_service")


class RefundService:
    """
    Business logic for refund flows.
    """

    # --------------------------------------------------------
    # REFUND TO WALLET
    # --------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def approve_wallet_refund(refund_id: str):

        refund = RefundRepository.lock_wallet_refund(refund_id)

        if refund.is_processed:
            raise ValidationError("Already processed.")

        wallet = WalletRepository.lock(refund.wallet.id)

        balance_before = wallet.balance
        balance_after = balance_before + refund.amount

        transaction_obj = TransactionRepository.create(
            wallet=wallet,
            amount=refund.amount,
            transaction_type=TransactionType.REFUND_TO_WALLET,
            status=TransactionStatus.APPROVED,
            description=refund.reason,
        )

        LedgerRepository.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.REFUND_TO_WALLET,
            amount=refund.amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

        refund.transaction = transaction_obj

        RefundRepository.mark_wallet_refund_approved(refund)

        logger.info(f"Wallet refund approved | id={refund_id}")

        return refund

    @staticmethod
    @transaction.atomic
    def reject_wallet_refund(refund_id: str, note: str = ""):

        refund = RefundRepository.lock_wallet_refund(refund_id)

        if refund.is_processed:
            raise ValidationError("Already processed.")

        RefundRepository.mark_wallet_refund_rejected(refund, note)

        logger.info(f"Wallet refund rejected | id={refund_id}")

        return refund

    # --------------------------------------------------------
    # REFUND TO USER
    # --------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def approve_user_refund(refund_id: str):

        refund = RefundRepository.lock_user_refund(refund_id)

        if refund.is_processed:
            raise ValidationError("Already processed.")

        wallet = WalletRepository.lock(refund.wallet.id)

        if wallet.balance < refund.amount:
            raise ValidationError("Insufficient balance.")

        balance_before = wallet.balance
        balance_after = balance_before - refund.amount

        transaction_obj = TransactionRepository.create(
            wallet=wallet,
            amount=refund.amount,
            transaction_type=TransactionType.REFUND_TO_USER,
            status=TransactionStatus.APPROVED,
            description=refund.reason,
        )

        LedgerRepository.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.REFUND_TO_USER,
            amount=-refund.amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

        refund.transaction = transaction_obj

        RefundRepository.mark_user_refund_approved(refund)

        logger.info(f"User refund approved | id={refund_id}")

        return refund

    @staticmethod
    @transaction.atomic
    def reject_user_refund(refund_id: str, note: str = ""):

        refund = RefundRepository.lock_user_refund(refund_id)

        if refund.is_processed:
            raise ValidationError("Already processed.")

        RefundRepository.mark_user_refund_rejected(refund, note)

        logger.info(f"User refund rejected | id={refund_id}")

        return refund
