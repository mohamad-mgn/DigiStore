from django.urls import path
from .views import HomeView, AboutView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path("about/", AboutView.as_view(), name="about"),
]