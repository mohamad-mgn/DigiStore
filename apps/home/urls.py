from django.urls import path
from .views import HomeView, AboutView

# --------------------------------------------------------
# Namespace for the 'home' app URLs
# --------------------------------------------------------
app_name = 'home'

# --------------------------------------------------------
# URL patterns for main pages
# --------------------------------------------------------
urlpatterns = [
    # Homepage
    path('', HomeView.as_view(), name='index'),

    # About page
    path("about/", AboutView.as_view(), name="about"),
]