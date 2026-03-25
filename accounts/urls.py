from django.urls import path

from .views import (
    AccountLoginView,
    AccountLogoutView,
    ProfileUpdateView,
    ProfileView,
    SecuritySettingsView,
    SignUpView,
)


app_name = "accounts"

urlpatterns = [
    path("login/", AccountLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("security/", SecuritySettingsView.as_view(), name="security"),
]
