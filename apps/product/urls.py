from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView
)

app_name = "product"

urlpatterns = [
    # Display all products
    path("", ProductListView.as_view(), name="list"),

    # Product detail page
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),

    # Display products by category
    path("category/<slug:slug>/", ProductListView.as_view(), name="category"),

    # Product search page
    path("search/", ProductListView.as_view(), name="search"),

    # Seller creates a new product
    path("seller/create/", ProductCreateView.as_view(), name="create"),

    # Seller updates an existing product
    path("seller/<int:pk>/update/", ProductUpdateView.as_view(), name="update"),

    # Seller deletes a product
    path("seller/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete"),
]