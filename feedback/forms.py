from django import forms

from common.forms import BootstrapFormMixin

from .models import FeedbackEntry


class FeedbackForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FeedbackEntry
        fields = ("name", "email", "category", "message")
        labels = {
            "name": "姓名",
            "email": "邮箱",
            "category": "反馈类型",
            "message": "反馈内容",
        }


class FeedbackStatusForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FeedbackEntry
        fields = ("status",)
        labels = {
            "status": "处理状态",
        }
