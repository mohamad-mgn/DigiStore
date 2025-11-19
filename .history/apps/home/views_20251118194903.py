from django.views.generic import TemplateView
from apps.product.models import Product, Category


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["latest_products"] = Product.objects.select_related("category", "store").order_by('-id')[:8]

        ctx["categories"] = Category.objects.all()

        return ctx