from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView
)

app_name = "product"

urlpatterns = [

    # PUBLIC
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),

    # SELLER ACTIONS
    path("seller/create/", ProductCreateView.as_view(), name="create"),
    path("seller/<int:pk>/update/", ProductUpdateView.as_view(), name="update"),
    path("seller/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete"),
]