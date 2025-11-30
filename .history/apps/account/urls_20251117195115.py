from django.urls import path
from .views import (
    SendOTPView,
    VerifyOTPView,
    SignupView,
    SigninView,
    SignoutView,
    ProfileView,
    ProfileEditView,
)


app_name = "account"

urlpatterns = [
    path("send-otp/", SendOTPView.as_view(), name="send_otp"),
    path("verify/<str:phone>/", VerifyOTPView.as_view(), name="verify_otp"),
    path("signup/<str:phone>/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("signout/", SignoutView.as_view(), name="signout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
]