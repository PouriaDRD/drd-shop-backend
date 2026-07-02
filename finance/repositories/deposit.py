from django.db import transaction
from django.db.models import QuerySet

from finance.enums import DepositStatus
from finance.models import DepositRequestModel, TransactionModel, WalletModel


class DepositRepository:
    """
    Repository layer for deposit requests.

    Responsible only for database operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        wallet: WalletModel,
        **kwargs,
    ) -> DepositRequestModel:
        """
        Create a new deposit request.
        """

        return DepositRequestModel.objects.create(wallet=wallet, **kwargs)

    @staticmethod
    def get_by_id(
        deposit_id,
    ) -> DepositRequestModel | None:
        """
        Retrieve a deposit request by id.
        """

        return (
            DepositRequestModel.objects.select_related(
                "transaction",
                "transaction__wallet",
            )
            .filter(id=deposit_id)
            .first()
        )

    @staticmethod
    def get_user_requests(wallet_id) -> QuerySet[DepositRequestModel]:
        """
        Return all deposit requests for a wallet.
        """

        return (
            DepositRequestModel.objects.filter(
                transaction__wallet_id=wallet_id,
            )
            .select_related(
                "transaction",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_wallet_deposits(
        wallet_id: str,
    ) -> QuerySet[DepositRequestModel]:
        """
        Retrieve all deposit requests belonging to a wallet.
        """

        return (
            DepositRequestModel.objects.filter(wallet_id=wallet_id)
            .select_related(
                "wallet",
                "wallet__user",
                "transaction",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_pending() -> QuerySet[DepositRequestModel]:
        """
        Retrieve all pending deposit requests.
        """

        return (
            DepositRequestModel.objects.filter(
                is_processed=False,
            )
            .select_related(
                "wallet",
                "wallet__user",
                "transaction",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def lock(
        deposit_id,
    ) -> DepositRequestModel:
        """
        Lock deposit request.

        Must be called inside transaction.atomic().
        """

        return (
            DepositRequestModel.objects.select_for_update()
            .select_related(
                "transaction",
                "transaction__wallet",
            )
            .get(id=deposit_id)
        )

    @staticmethod
    @transaction.atomic
    def approve(
        deposit: DepositRequestModel,
    ) -> DepositRequestModel:
        """
        Mark deposit as approved.
        """

        deposit.status = DepositStatus.APPROVED
        deposit.is_processed = True

        deposit.save(
            update_fields=[
                "status",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        return deposit

    @staticmethod
    @transaction.atomic
    def reject(
        deposit: DepositRequestModel,
        admin_note: str = "",
    ) -> DepositRequestModel:
        """
        Mark deposit as rejected.
        """

        deposit.status = DepositStatus.REJECTED
        deposit.is_processed = True
        deposit.admin_note = admin_note

        deposit.save(
            update_fields=[
                "status",
                "admin_note",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        return deposit

    @staticmethod
    @transaction.atomic
    def attach_transaction(
        deposit: DepositRequestModel,
        transaction: TransactionModel,
    ) -> DepositRequestModel:
        """
        Attach parent transaction.
        """

        deposit.transaction = transaction

        deposit.save(
            update_fields=[
                "transaction",
                "updated_at",
            ]
        )

        return deposit
