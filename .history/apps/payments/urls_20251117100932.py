from django.urls import path
from .views import InitiatePaymentView, MockPaymentPage

app_name = "payments"

urlpatterns = [
    path("initiate/<int:order_id>/", InitiatePaymentView.as_view(), name="initiate"),
    # صفحه شبیه‌سازی که یک فرم دارد برای success/fail
    path("mock-pay/<int:payment_id>/", MockPaymentPage.as_view(), name="mock"),
]