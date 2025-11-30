from django.urls import path
from .views import AddToCartView, CartView, UpdateCartItemView, RemoveCartItemView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart_view'),
    path('add/<int:product_pk>/', AddToCartView.as_view(), name='add'),
    path('item/<int:item_pk>/update/', UpdateCartItemView.as_view(), name='item_update'),
    path('item/<int:item_pk>/remove/', RemoveCartItemView.as_view(), name='item_remove'),
]