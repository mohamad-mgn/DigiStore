from django.views.generic import TemplateView
from apps.product.models import Product, Category

# --------------------------------------------------------
# Homepage view
# --------------------------------------------------------
class HomeView(TemplateView):
    """
    Displays the homepage with the latest products and all categories.
    """
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Fetch the latest 8 products, including related category and store to optimize queries
        ctx["latest_products"] = Product.objects.select_related("category", "store").order_by('-id')[:8]

        # Fetch all product categories
        ctx["categories"] = Category.objects.all()

        return ctx


# --------------------------------------------------------
# About page view
# --------------------------------------------------------
class AboutView(TemplateView):
    """
    Displays the 'About' page.
    """
    template_name = "home/about.html"