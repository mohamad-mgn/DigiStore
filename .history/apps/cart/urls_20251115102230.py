from django.urls import path
from .views import add_to_cart, cart_detail, remove_item

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_pk>/', add_to_cart, name='add_to_cart'),
    path('', cart_detail, name='cart_detail'),
    path('remove/<int:item_pk>/', remove_item, name='remove_item'),
]