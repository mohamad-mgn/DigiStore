from django.contrib import admin
from django.urls import path, include
from apps.home.views import HomeView
from django.conf import settings
from django.conf.urls.static import static

# URL configuration for the entire Django project.
# Each path here maps a URL prefix to the corresponding app's URLs or view.

urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),

    # Home app URLs, handles the homepage and related pages
    path("", include("apps.home.urls", namespace="home")),

    # Account app URLs, handles user authentication, signup, signin, etc.
    path("account/", include("apps.account.urls", namespace="account")),

    # Product app URLs, manages product listings, details, categories
    path("product/", include("apps.product.urls", namespace="product")),

    # Store app URLs, handles store management and seller-related pages
    path("store/", include("apps.store.urls", namespace="store")),

    # Cart app URLs, manages shopping cart functionalities
    path("cart/", include("apps.cart.urls", namespace="cart")),

    # Orders app URLs, manages order creation, tracking, and history
    path("orders/", include("apps.orders.urls", namespace="orders")),

    # Payments app URLs, handles payment processing and payment status
    path("payments/", include("apps.payments.urls", namespace="payments")),

    # Dashboard app URLs, admin or user dashboard features
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
]

# Serving static and media files in development mode
# This should only be used when DEBUG=True (i.e., in local development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)