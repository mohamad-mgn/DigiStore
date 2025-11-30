from django.urls import path
from .views import (
    CustomerDashboardView,
    SellerDashboardView
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
]