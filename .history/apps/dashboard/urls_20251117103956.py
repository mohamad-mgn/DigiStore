from django.urls import path
from .views import (
    CustomerDashboardView,
    SellerDashboardView
)

app_name = "dashboard"

urlpatterns = [
    path("customer/", CustomerDashboardView.as_view(), name="customer"),
    path("seller/", SellerDashboardView.as_view(), name="seller"),
]