from django.shortcuts import render
from apps.product.models import Product

def home(request):
    latest_products = Product.objects.all().order_by('-id')[:8]
    return render(request, 'home/index.html', {
        'latest_products': latest_products
    })