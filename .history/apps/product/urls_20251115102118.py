from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDetailView

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/<int:store_pk>/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]