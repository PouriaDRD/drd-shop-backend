import logging

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from finance.enums import (
    DepositStatus,
    TransactionStatus,
    TransactionType,
)
from finance.models import DepositRequestModel, WalletModel
from finance.repositories import (
    DepositRepository,
    LedgerRepository,
    TransactionRepository,
    WalletRepository,
)

logger = logging.getLogger("finance.deposit_service")


class DepositService:
    """
    Business logic for deposit requests.
    """

    @staticmethod
    def create(wallet: WalletModel, **validated_data) -> DepositRequestModel:
        """
        Create a new deposit request.

        The request is created with PENDING status.
        No wallet balance is changed here.
        """

        deposit = DepositRepository.create(wallet, **validated_data)

        logger.info(
            f"Deposit request created | id={deposit.id} amount={deposit.amount}",
        )

        return deposit

    @staticmethod
    @transaction.atomic
    def approve(
        deposit_id,
    ) -> DepositRequestModel:
        """
        Approve a deposit request.

        Flow:

            Lock Deposit
                    ↓
            Validate State
                    ↓
            Lock Wallet
                    ↓
            Create Transaction
                    ↓
            Update Wallet Balance
                    ↓
            Create Ledger Entry
                    ↓
            Approve Transaction
                    ↓
            Approve Deposit
        """

        deposit = DepositRepository.lock(deposit_id)

        if deposit.is_processed:
            raise ValidationError("Deposit request has already been processed.")

        wallet = WalletRepository.lock(
            deposit.wallet.id,
        )

        balance_before = wallet.balance
        balance_after = balance_before + deposit.amount

        transaction_obj = TransactionRepository.create(
            wallet=wallet,
            amount=deposit.amount,
            transaction_type=TransactionType.DEPOSIT,
            status=TransactionStatus.APPROVED,
            description=deposit.note or "تراکنش واریز",
        )

        LedgerRepository.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.DEPOSIT,
            amount=deposit.amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

        deposit.transaction = transaction_obj
        deposit.status = DepositStatus.APPROVED
        deposit.is_processed = True
        deposit.reviewed_at = timezone.now()

        deposit.save(
            update_fields=[
                "transaction",
                "status",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        logger.info(
            f"Deposit approved | deposit={deposit.id} transaction={transaction_obj.id}",
        )

        return deposit

    @staticmethod
    @transaction.atomic
    def reject(
        deposit_id,
        *,
        admin_note: str = "",
    ) -> DepositRequestModel:
        """
        Reject deposit request.

        No wallet balance changes.
        """

        deposit = DepositRepository.lock(
            deposit_id,
        )

        if deposit.is_processed:
            raise ValidationError("Deposit request has already been processed.")

        deposit.admin_note = admin_note
        deposit.status = DepositStatus.REJECTED
        deposit.is_processed = True
        deposit.reviewed_at = timezone.now()

        deposit.save(
            update_fields=[
                "admin_note",
                "status",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        logger.info(
            f"Deposit rejected | deposit={deposit.id}",
        )

        return deposit
