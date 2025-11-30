from django.urls import path
from .views import (
    UserOrderListView, OrderDetailView, CheckoutView,
    SellerOrderListView, SellerUpdateOrderStatusView,
    PaymentView
)

app_name = "orders"

# --------------------------------------------------------
# URL patterns for the orders app
# --------------------------------------------------------
urlpatterns = [
    # List of orders for the logged-in customer
    path("", UserOrderListView.as_view(), name="user_orders"),

    # Detailed view of a specific order by its ID
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),

    # Checkout page to create an order from the cart
    path("checkout/", CheckoutView.as_view(), name="checkout"),

    # List of orders for the logged-in seller
    path("seller/", SellerOrderListView.as_view(), name="seller_orders"),

    # Update the status of a specific order (seller view)
    path("seller/<int:pk>/update-status/", SellerUpdateOrderStatusView.as_view(), name="seller_update_status"),

    # Payment of orders
    path("<int:pk>/payment,", PaymentView.as_view(), name="payment"),
]