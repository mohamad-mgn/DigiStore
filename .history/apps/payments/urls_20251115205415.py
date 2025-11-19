from django.urls import path
from .views import PaymentView

app_name = 'payments'

urlpatterns = [
    path('pay/<int:order_id>/', PaymentView.as_view(), name='pay'),
]