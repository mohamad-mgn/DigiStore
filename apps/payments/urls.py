from django.urls import path
from .views import InitiatePaymentView, MockPaymentPage

app_name = "payments"

urlpatterns = [
    # URL to initiate a payment for a given order
    path("initiate/<int:order_id>/", InitiatePaymentView.as_view(), name="initiate"),

    # URL to simulate the payment page (mock)
    path("mock-pay/<int:payment_id>/", MockPaymentPage.as_view(), name="mock"),
]