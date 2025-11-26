from apps.cart.models import Cart
from apps.cart.utils import get_or_create_cart
from apps.store.models import Store

# --------------------------------------------------------
# Global context processor for templates
# --------------------------------------------------------
def global_context(request):
    """
    Provide common context variables for all templates.
    Includes cart item count, authentication status, seller/store info, and user name.
    """
    user = getattr(request, "user", None)
    cart_item_count = 0
    is_seller = False
    store_exists = False
    user_name = None

    # Check if the user is authenticated
    if user and user.is_authenticated:
        is_seller = getattr(user, "is_seller", False)
        user_name = getattr(user, "full_name", None) or user.phone

        # Attempt to get the user's cart and count items
        try:
            cart = Cart.objects.filter(user=user).first()
            if cart:
                cart_item_count = cart.items.count()
        except Exception:
            cart_item_count = 0

        # If user is a seller, check if they have an associated store
        if is_seller:
            try:
                store_exists = Store.objects.filter(seller=user).exists()
            except Exception:
                store_exists = False

    return {
        "cart_item_count": cart_item_count,
        "is_authenticated": user.is_authenticated if user else False,
        "is_seller": is_seller,
        "store_exists": store_exists,
        "user_name": user_name,
    }


# --------------------------------------------------------
# Simplified global context for cart
# --------------------------------------------------------
def global_context(request):
    """
    Provide minimal cart context for templates.
    Uses a utility function to get or create the cart for the current session/user.
    """
    cart = get_or_create_cart(request)
    cart_count = cart.items.count() if cart else 0

    return {
        "cart_count": cart_count
    }