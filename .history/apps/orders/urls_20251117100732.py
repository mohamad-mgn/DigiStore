from django.urls import path
from .views import (
    UserOrderListView, OrderDetailView, CheckoutView,
    SellerOrderListView, SellerUpdateOrderStatusView
)

app_name = "orders"

urlpatterns = [
    path("", UserOrderListView.as_view(), name="user_orders"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),

    # Seller
    path("seller/", SellerOrderListView.as_view(), name="seller_orders"),
    path("seller/<int:pk>/update-status/", SellerUpdateOrderStatusView.as_view(), name="seller_update_status"),
]