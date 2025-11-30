from django.urls import path
from .views import StoreDetailView, StoreUpdateView

app_name = "store"

urlpatterns = [
    path("<int:pk>/", StoreDetailView.as_view(), name="detail"),
    path("edit/", StoreUpdateView.as_view(), name="edit"),
]