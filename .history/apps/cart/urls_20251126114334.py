from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartItemView,
    ClearCartView,
)

# --------------------------------------------------------
# Namespace for the 'cart' app URLs
# --------------------------------------------------------
app_name = "cart"

# --------------------------------------------------------
# URL patterns for cart-related views
# --------------------------------------------------------
urlpatterns = [
    # View the current cart
    path("", CartView.as_view(), name="detail"),

    # Add a product to the cart by product ID
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add"),

    # Remove a specific cart item by item ID
    path("remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove"),

    # Update quantity of a specific cart item by item ID
    path("update/<int:item_id>/", UpdateCartItemView.as_view(), name="update"),

    # Clear all items from the cart
    path("clear/", ClearCartView.as_view(), name="clear"),
]