from django.urls import path
from .views import (
    StoreListView,
    StoreDetailView,
    StoreCreateView,
    StoreUpdateView,
    StoreDeleteView,
)

app_name = "store"

urlpatterns = [
    path("", StoreListView.as_view(), name="list"),
    path("<int:pk>/", StoreDetailView.as_view(), name="detail"),
    path("create/", StoreCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", StoreUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", StoreDeleteView.as_view(), name="delete"),
]