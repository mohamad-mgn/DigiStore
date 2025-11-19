from django.urls import path
from .views import MyStoresView, StoreCreateView, StoreDetailView

app_name = 'store'

urlpatterns = [
    path('my/', MyStoresView.as_view(), name='my_stores'),
    path('create/', StoreCreateView.as_view(), name='store_create'),
    path('<slug:slug>/', StoreDetailView.as_view(), name='store_detail'),
]