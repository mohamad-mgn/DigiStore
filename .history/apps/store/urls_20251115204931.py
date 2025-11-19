from django.urls import path
from .views import (
    StoreCreateView,
    MyStoreView,
    StoreDetailView,
    StoreProductListView,
)

app_name = "store"

urlpatterns = [
    path("create/", StoreCreateView.as_view(), name="create"),
    path("my/", MyStoreView.as_view(), name="my_store"),
    path("<int:pk>/", StoreDetailView.as_view(), name="detail"),
    path("<int:store_id>/products/", StoreProductListView.as_view(), name="products"),
]