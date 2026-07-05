import logging

from django.db import transaction
from rest_framework.exceptions import ValidationError

from finance.models import DepositRequestModel, WalletModel
from finance.enums import TransactionStatus, TransactionType
from finance.repositories import DepositRepository, WalletRepository

from .ledger import LedgerService
from .transaction import TransactionService

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
            f"Deposit request created | id={str(deposit.id)} amount={deposit.amount}",
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

        wallet = WalletRepository.lock(deposit.wallet.id)

        amount = deposit.amount

        transaction_obj = TransactionService.create(
            wallet=wallet,
            amount=amount,
            transaction_type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
            description="تراکنش واریز",
        )

        TransactionService.approve(str(transaction_obj.id))

        LedgerService.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
        )

        DepositRepository.approve(deposit, transaction_obj)

        logger.info(
            f"Deposit approved: id={str(deposit.id)}, user={str(deposit.wallet.user)}, amount={amount}",
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

        DepositRepository.reject(deposit, admin_note)

        logger.info(
            f"Deposit rejected: id={str(deposit.id)}, user={str(deposit.wallet.user)}",
        )

        return deposit
