import logging
from typing import Optional
from django.db import transaction
from rest_framework.exceptions import ValidationError

from notifications.enums import NotificationType
from notifications.services import NotificationService

from finance.enums import (
    TransactionType,
    TransactionStatus,
)
from finance.repositories import WalletRepository
from finance.models import TransactionModel, WalletModel, RefundToWalletRequestModel

from .ledger import LedgerService
from .transaction import TransactionService

from finance.repositories import RefundRepository

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
    def create_wallet_refund(
        wallet: WalletModel,
        amount: int,
        reason: str = "",
        **kwargs,
    ) -> RefundToWalletRequestModel:
        return RefundRepository.create_wallet_refund(
            wallet=wallet,
            amount=amount,
            reason=reason,
            **kwargs,
        )

    @staticmethod
    @transaction.atomic
    def approve_wallet_refund(
        refund_id: str, perv_tx: Optional[TransactionModel] = None
    ):

        refund = RefundRepository.lock_wallet_refund(refund_id)

        if refund.is_processed:
            raise ValidationError("Wallet refund has already been processed.")

        wallet = WalletRepository.lock(refund.wallet.id)
        amount = refund.amount

        if perv_tx:
            TransactionService.reject(str(perv_tx.id))

        transaction_obj = TransactionService.create(
            wallet=wallet,
            amount=amount,
            transaction_type=TransactionType.REFUND_TO_WALLET,
            status=TransactionStatus.PENDING,
            description=refund.reason or "تراکنش استرداد",
        )

        tx = TransactionService.approve(str(transaction_obj.id))

        LedgerService.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.REFUND_TO_WALLET,
            amount=amount,
        )

        RefundRepository.approve_wallet_refund(refund, tx)

        logger.info(
            f"Wallet refund approved: id={str(refund_id)}, user={str(refund.wallet.user)}, amount={amount}"
        )

        return refund

    @staticmethod
    @transaction.atomic
    def reject_wallet_refund(refund_id: str, note: str = ""):

        refund = RefundRepository.lock_wallet_refund(refund_id)

        if refund.is_processed:
            raise ValidationError("Wallet refund has already been processed.")

        RefundRepository.reject_wallet_refund(refund, note)

        logger.info(
            f"Wallet refund rejected: id={str(refund_id)}, user={str(refund.wallet.user)}"
        )

        return refund

    # --------------------------------------------------------
    # REFUND TO USER
    # --------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def approve_user_refund(refund_id: str):

        refund = RefundRepository.lock_user_refund(refund_id)

        if refund.is_processed:
            raise ValidationError("User refund has already been processed.")

        wallet = WalletRepository.lock(refund.wallet.id)
        amount = refund.amount

        if wallet.balance < amount:
            raise ValidationError("Insufficient balance.")

        transaction_obj = TransactionService.create(
            wallet=wallet,
            amount=amount,
            transaction_type=TransactionType.REFUND_TO_USER,
            status=TransactionStatus.PENDING,
            description=refund.reason or "تراکنش استرداد",
        )

        tx = TransactionService.approve(str(transaction_obj.id))

        LedgerService.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.REFUND_TO_USER,
            amount=-amount,
        )

        RefundRepository.approve_user_refund(refund, tx)

        NotificationService.create_success(
            user=wallet.user,
            title="تراکنش استرداد تایید شد",
            message="تراکنش استرداد با موفقیت تایید شد، مبلغ آن به حساب بانکی شما برگشت داده شد!",
            notification_type=NotificationType.INFO,
        )

        logger.info(
            f"User refund approved: id={str(refund_id)}, user:{str(refund.wallet.user)}, amount={amount}"
        )

        return refund

    @staticmethod
    @transaction.atomic
    def reject_user_refund(refund_id: str, note: str = ""):

        refund = RefundRepository.lock_user_refund(refund_id)

        if refund.is_processed:
            raise ValidationError("User refund has already been processed.")

        RefundRepository.reject_user_refund(refund, note)

        logger.info(
            f"User refund rejected: id={str(refund_id)}, user:{str(refund.wallet.user)}"
        )

        return refund
