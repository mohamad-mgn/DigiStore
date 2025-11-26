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
    # List all stores
    path("", StoreListView.as_view(), name="list"),
    
    # View store details by store ID
    path("<int:pk>/", StoreDetailView.as_view(), name="detail"),
    
    # Create a new store
    path("create/", StoreCreateView.as_view(), name="create"),
    
    # Update a store by store ID
    path("<int:pk>/edit/", StoreUpdateView.as_view(), name="edit"),
    
    # Delete a store by store ID
    path("<int:pk>/delete/", StoreDeleteView.as_view(), name="delete"),
]