from accounts.models import UserModel
from shop.enums import OrderStatus
from shop.models import OrderModel


class OrderRepository:
    """
    Order database operations.
    """

    @staticmethod
    def create(
        *,
        user: UserModel,
        status: OrderStatus = OrderStatus.PENDING,
        total_price: int = 0,
    ) -> OrderModel:
        return OrderModel.objects.create(
            user=user,
            status=status,
            total_price=total_price,
        )

    @staticmethod
    def get(user: UserModel) -> OrderModel | None:
        return (
            OrderModel.objects.prefetch_related(
                "items",
                "items__product",
                "items__plan",
            )
            .filter(user=user)
            .first()
        )

    @staticmethod
    def save(order: OrderModel) -> OrderModel:
        order.save()
        return order
