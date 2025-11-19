from django.urls import path
from .views import pay_view

app_name = 'payments'

urlpatterns = [
    path('pay/', pay_view, name='pay'),
]