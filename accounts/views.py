from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from .forms import LoginForm, SecuritySettingsForm, SignUpForm, UserProfileForm
from .models import UserProfile


class AccountLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView):
    pass


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("dashboard:index")

    def dispatch(self, request, *args, **kwargs):
        # Registration only serves anonymous users; logged-in users should not
        # be able to re-enter the signup flow.
        if request.user.is_authenticated:
            return redirect("dashboard:index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # The profile row is created alongside the auth user so later profile
        # pages can safely assume a matching UserProfile exists.
        UserProfile.objects.get_or_create(
            user=self.object,
            defaults={"contact_email": self.object.email},
        )
        login(self.request, self.object)
        messages.success(self.request, "注册成功，欢迎进入 AeroVision。")
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Old accounts or admin-created users may not have a profile row yet,
        # so the page provisions it lazily on first access.
        profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={"contact_email": self.request.user.email},
        )
        context["profile"] = profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        # Reuse the same lazy profile creation rule used by the read-only page.
        profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={"contact_email": self.request.user.email},
        )
        return profile

    def form_valid(self, form):
        messages.success(self.request, "个人资料已更新。")
        return super().form_valid(form)


class SecuritySettingsView(LoginRequiredMixin, FormView):
    form_class = SecuritySettingsForm
    template_name = "accounts/security.html"
    success_url = reverse_lazy("accounts:security")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # PasswordChangeForm needs the current authenticated user instance.
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        # Keep the session valid after a password change so the user is not
        # forced to log in again from the settings page.
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "密码已更新，当前登录状态已保留。")
        return super().form_valid(form)
