from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

from common.forms import BootstrapFormMixin

from .models import UserProfile


User = get_user_model()


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="邮箱")
    first_name = forms.CharField(label="姓名", max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "password1", "password2")


class UserProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("display_name", "title", "organization", "contact_email", "bio")
        labels = {
            "display_name": "显示名称",
            "title": "职位 / 角色",
            "organization": "所属单位",
            "contact_email": "联系邮箱",
            "bio": "个人简介",
        }


class SecuritySettingsForm(BootstrapFormMixin, PasswordChangeForm):
    pass
