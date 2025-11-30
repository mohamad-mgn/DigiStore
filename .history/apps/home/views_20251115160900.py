from django.views.generic import ListView
from apps.product.models import Product

class HomeView(ListView):
    model = Product
    template_name = 'home/index.html'
    context_object_name = 'latest_products'
    queryset = Product.objects.all().order_by('-id')[:8]