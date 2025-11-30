from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView
)

app_name = "product"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),

    # Seller actions
    path("create/", ProductCreateView.as_view(), name="create"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="delete"),
]