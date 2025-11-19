# digistore/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # صفحات اصلی
    path("", include("apps.home.urls", namespace="home")),

    # اپ‌ها
    path("account/", include("apps.account.urls", namespace="account")),
    path("product/", include("apps.product.urls", namespace="product")),
    path("store/", include("apps.store.urls", namespace="store")),
    path("cart/", include("apps.cart.urls", namespace="cart")),
    path("orders/", include("apps.orders.urls", namespace="orders")),
    path("payments/", include("apps.payments.urls", namespace="payments")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
]

# سرو کردن فایل‌های static/media در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])