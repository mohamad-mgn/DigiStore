from django.urls import path
from .views import ProfileView, ProfileEditView

app_name = "user"

# URL patterns for user profile views
urlpatterns = [
    # View for displaying the user's profile
    path("profile/", ProfileView.as_view(), name="profile"),

    # View for editing the user's profile
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
]