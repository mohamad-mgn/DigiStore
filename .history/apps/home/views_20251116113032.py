from django.views.generic import ListView
from apps.product.models import Product


class HomeView(ListView):
    model = Product
    template_name = 'home/index.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        """
        جدیدترین محصولات (۸ عدد آخر)
        """
        return Product.objects.order_by('-id')[:8]