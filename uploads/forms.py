from django import forms

from common.forms import BootstrapFormMixin

from .models import UploadAsset


class UploadForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UploadAsset
        fields = ("title", "description", "asset")
        labels = {
            "title": "文件标题",
            "description": "文件描述",
            "asset": "选择文件",
        }
