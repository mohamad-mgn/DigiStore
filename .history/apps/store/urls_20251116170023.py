from django.urls import path
from .views import (
    StoreListView, StoreDetailView,
    StoreCreateView, StoreUpdateView, StoreDeleteView
)

app_name = "store"

urlpatterns = [
    path("", StoreListView.as_view(), name="list"),
    path("<slug:slug>/", StoreDetailView.as_view(), name="detail"),

    # Seller actions
    path("create/", StoreCreateView.as_view(), name="create"),
    path("<slug:slug>/update/", StoreUpdateView.as_view(), name="update"),
    path("<slug:slug>/delete/", StoreDeleteView.as_view(), name="delete"),
]