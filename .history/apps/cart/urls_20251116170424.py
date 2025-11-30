from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartItemView,
    ClearCartView,
)

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="view"),
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add"),
    path("remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove"),
    path("update/<int:item_id>/", UpdateCartItemView.as_view(), name="update"),
    path("clear/", ClearCartView.as_view(), name="clear"),
]