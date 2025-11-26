from apps.cart.models import Cart, CartItem
from .models import Order, OrderItem
from django.db import transaction

# --------------------------------------------------------
# Order service
# --------------------------------------------------------
class OrderService:
    """
    Service class for handling order-related operations.
    Provides methods to create orders from a user's cart.
    """

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user, address=None, postal_code=None) -> Order:
        """
        Creates a new order based on the user's current cart.

        Steps:
        1. Fetch the user's cart and items.
        2. Calculate total amount.
        3. Create the Order instance.
        4. Create OrderItem instances for each cart item.
        5. Deduct stock for each product.
        6. Clear the cart.

        Args:
            user: The User object placing the order.
            address: Optional delivery address.
            postal_code: Optional postal code.

        Returns:
            Order: The newly created Order instance.

        Raises:
            ValueError: If the cart is empty or product stock is insufficient.
        """

        # Retrieve user's cart or create a new one
        cart, _ = Cart.objects.get_or_create(user=user)
        items = cart.items.select_related('product').all()

        if not items:
            raise ValueError("سبد خرید خالی است.")  # Cart is empty

        # Calculate total price
        total = sum(item.product.price * item.quantity for item in items)

        # Create the order
        order = Order.objects.create(
            user=user,
            status='pending',
            total_amount=total,
            address=address,
            postal_code=postal_code
        )

        # Prepare order items
        order_items = []
        for it in items:
            order_items.append(OrderItem(
                order=order,
                product=it.product,
                unit_price=it.product.price,
                quantity=it.quantity
            ))

            # Deduct product stock
            if it.product.stock >= it.quantity:
                it.product.stock -= it.quantity
                it.product.save(update_fields=['stock'])
            else:
                raise ValueError(f"موجودی کافی برای {it.product.title} وجود ندارد.")  # Insufficient stock

        # Bulk create order items
        OrderItem.objects.bulk_create(order_items)

        # Clear cart after order creation
        cart.items.all().delete()

        return order