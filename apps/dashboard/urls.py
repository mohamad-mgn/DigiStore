from django.urls import path
from .views import (
    CustomerDashboardView,
    SellerDashboardView,
    SellerStockView
)

# --------------------------------------------------------
# Namespace for the 'dashboard' app URLs
# --------------------------------------------------------
app_name = "dashboard"

# --------------------------------------------------------
# URL patterns for dashboard views
# --------------------------------------------------------
urlpatterns = [
    # Dashboard for customers
    path("customer/", CustomerDashboardView.as_view(), name="customer"),

    # Dashboard for sellers
    path("seller/", SellerDashboardView.as_view(), name="seller"),

    # Product's stock for sellers
    path("stock/", SellerStockView.as_view(), name="seller_stock"),
]