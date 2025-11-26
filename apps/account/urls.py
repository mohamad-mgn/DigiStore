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

# --------------------------------------------------------
# Namespace for the 'account' app URLs
# --------------------------------------------------------
app_name = "account"

# --------------------------------------------------------
# URL patterns for account-related views
# --------------------------------------------------------
urlpatterns = [
    # Send OTP to the given phone number
    path("send-otp/", SendOTPView.as_view(), name="send_otp"),

    # Verify OTP for a specific phone number
    path("verify/<str:phone>/", VerifyOTPView.as_view(), name="verify_otp"),

    # Final signup for a given phone number
    path("signup/<str:phone>/", SignupView.as_view(), name="signup"),

    # User sign-in
    path("signin/", SigninView.as_view(), name="signin"),

    # User sign-out
    path("signout/", SignoutView.as_view(), name="signout"),

    # View user profile
    path("profile/", ProfileView.as_view(), name="profile"),

    # Edit user profile
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
]