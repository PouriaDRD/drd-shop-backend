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
    @transaction.atomic
    def create(**validated_data) -> PurchaseRequestModel:
        """
        Create purchase request.
        """

        amount = int(validated_data["amount"])
        reason = validated_data.get("reason", "تراکنش خرید")
        wallet = WalletRepository.lock(validated_data["wallet"].id)

        if wallet.balance < amount:
            raise ValidationError("موجودی کافی نیست")

        transaction_obj = TransactionRepository.create(
            wallet=wallet,
            amount=amount,
            transaction_type=TransactionType.PURCHASE,
            status=TransactionStatus.PENDING,
            description=reason,
        )

        balance_before = wallet.balance
        balance_after = balance_before - amount

        LedgerRepository.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.PURCHASE,
            amount=-amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

        validated_data["transaction"] = transaction_obj

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
            raise ValidationError("قبلا بررسی شده است.")

        purchase.status = PurchaseStatus.APPROVED
        purchase.is_processed = True
        purchase.reviewed_at = timezone.now()

        if purchase.transaction:
            TransactionRepository.approve(purchase.transaction)

        purchase.save(
            update_fields=[
                "status",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        logger.info(
            f"Purchase approved | id={purchase.id}",
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
