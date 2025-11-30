from django.urls import path
from .views import (
    send_otp_view,
    verify_otp_view,
    signup_view,
    signin_view,
    signout_view,
    profile_view,
    profile_edit_view,
)

app_name = "account"

urlpatterns = [
    path("send-otp/", send_otp_view, name="send_otp"),
    path("verify/<str:phone>/", verify_otp_view, name="verify_otp"),
    path("signup/<str:phone>/", signup_view, name="signup"),
    path("signin/", signin_view, name="signin"),
    path("signout/", signout_view, name="signout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),
]