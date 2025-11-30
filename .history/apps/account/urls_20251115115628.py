from django.urls import path
from .views import (
    signup_view,
    signin_view,
    verify_otp_view,
    logout_view,
    profile_view,
    profile_edit_view,
)

app_name = "account"

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('verify/', verify_otp_view, name='verify'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
]