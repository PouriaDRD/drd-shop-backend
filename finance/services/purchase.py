import logging

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from finance.enums import (
    TransactionType,
    TransactionStatus,
    PurchaseStatus,
)
from finance.models import PurchaseRequestModel

from finance.repositories import (
    PurchaseRepository,
    WalletRepository,
    TransactionRepository,
    LedgerRepository,
)

logger = logging.getLogger("finance.purchase_service")


class PurchaseService:
    """
    Business logic for purchase flow.

    Flow:
        Lock purchase
            ↓
        Lock wallet
            ↓
        Check balance
            ↓
        Create transaction (PENDING or APPROVED depending system)
            ↓
        Deduct wallet
            ↓
        Create ledger entry (negative amount)
            ↓
        Approve purchase
    """

    @staticmethod
    def create(**validated_data) -> PurchaseRequestModel:
        """
        Create purchase request.
        """

        purchase = PurchaseRepository.create(**validated_data)

        logger.info(
            f"Purchase created | id={purchase.id} wallet={purchase.wallet.id} amount={purchase.amount}",
        )

        return purchase

    @staticmethod
    @transaction.atomic
    def approve(purchase_id) -> PurchaseRequestModel:
        """
        Approve purchase and deduct wallet balance.
        """

        purchase = PurchaseRepository.lock(purchase_id)

        if purchase.is_processed:
            raise ValidationError("Purchase already processed.")

        wallet = WalletRepository.lock(purchase.wallet.id)

        if wallet.balance < purchase.amount:
            raise ValidationError("Insufficient balance.")

        balance_before = wallet.balance
        balance_after = balance_before - purchase.amount

        transaction_obj = TransactionRepository.create(
            wallet=wallet,
            amount=-purchase.amount,
            transaction_type=TransactionType.PURCHASE,
            status=TransactionStatus.APPROVED,
            description="Purchase approved.",
        )

        LedgerRepository.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.PURCHASE,
            amount=-purchase.amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

        purchase.transaction = transaction_obj
        purchase.status = PurchaseStatus.APPROVED
        purchase.is_processed = True
        purchase.reviewed_at = timezone.now()

        purchase.save(
            update_fields=[
                "transaction",
                "status",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        logger.info(
            f"Purchase approved | id={purchase.id} transaction={transaction_obj.id}",
        )

        return purchase

    @staticmethod
    @transaction.atomic
    def reject(purchase_id, *, admin_note: str = "") -> PurchaseRequestModel:
        """
        Reject purchase request.
        """

        purchase = PurchaseRepository.lock(purchase_id)

        if purchase.is_processed:
            raise ValidationError("Purchase already processed.")

        purchase.status = PurchaseStatus.REJECTED
        purchase.is_processed = True
        purchase.admin_note = admin_note
        purchase.reviewed_at = timezone.now()

        purchase.save(
            update_fields=[
                "status",
                "is_processed",
                "admin_note",
                "reviewed_at",
                "updated_at",
            ]
        )

        logger.info(
            f"Purchase rejected | id={purchase.id}",
        )

        return purchase
