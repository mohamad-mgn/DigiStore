from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView
)

app_name = "product"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),

    # فیلتر با slug (SEO Friendly)
    path("category/<slug:slug>/", ProductListView.as_view(), name="category"),

    # سرچ جداگانه
    path("search/", ProductListView.as_view(), name="search"),

    # seller actions
    path("seller/create/", ProductCreateView.as_view(), name="create"),
    path("seller/<int:pk>/update/", ProductUpdateView.as_view(), name="update"),
    path("seller/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete"),
]