from django.db import transaction

from ..coupon import CouponService
from accounts.models import UserModel
from shop.repositories.cart import CartRepository
from shop.repositories import CartItemRepository
from shop.models import CartModel, CartItemModel, ProductModel, ProductPlanModel


class CartService:
    """
    Business logic for cart.
    """

    @staticmethod
    def get_or_create_cart(user: UserModel):
        return CartRepository.get_or_create(user)

    @staticmethod
    @transaction.atomic
    def add_item(
        user: UserModel, *, product: ProductModel, plan: ProductPlanModel, quantity=1
    ):
        cart = CartService.get_or_create_cart(user)

        if not product.is_active:
            raise Exception("Product is not active.")

        if not plan.is_active:
            raise Exception("Plan is not active.")

        if not plan.is_available:
            raise Exception("Plan is not available.")

        item, created = cart.items.get_or_create(  # type: ignore
            product=product,
            plan=plan,
            defaults={
                "quantity": quantity,
                "unit_price": plan.price,
                "total_price": plan.price * quantity,
            },
        )

        if not created:
            item.quantity += quantity
            item.total_price = item.quantity * item.unit_price
            item.save()

        CartService.recalculate(cart)

        return cart, item

    @staticmethod
    @transaction.atomic
    def update_item(item: CartItemModel, *, quantity: int):
        item.quantity = quantity
        item.total_price = item.unit_price * quantity
        item.save()

        CartService.recalculate(item.cart)

        return item

    @staticmethod
    @transaction.atomic
    def remove_item(item: CartItemModel):
        cart = item.cart
        CartItemRepository.delete(item)
        CartService.recalculate(cart)
        return True

    @staticmethod
    def recalculate(cart: CartModel):
        items = cart.items.all()  # type: ignore

        subtotal = sum(i.total_price for i in items)

        discount = 0

        if cart.coupon:
            discount = CouponService.calculate_discount(
                cart.coupon,
                subtotal,
            )

        cart.subtotal = subtotal
        cart.discount = discount
        cart.total_price = max(subtotal - discount, 0)

        CartRepository.save(cart)

        return cart
