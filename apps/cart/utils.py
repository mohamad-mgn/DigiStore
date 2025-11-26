from .models import Cart

# --------------------------------------------------------
# Cart Utility Functions
# --------------------------------------------------------
def get_or_create_cart(request):
    """
    Retrieve the current user's cart or create a new one.

    - If the user is authenticated, the cart is tied to the user.
    - If the user is a guest, the cart is tied to the session key.
    """
    if request.user.is_authenticated:
        # Retrieve or create cart for logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    # Handle guest users with session-based cart
    session_key = request.session.session_key
    if not session_key:
        request.session.create()  # Create a new session if none exists
        session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart