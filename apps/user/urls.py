from django.urls import path
from .views import ProfileView, ProfileEditView

app_name = "user"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
]