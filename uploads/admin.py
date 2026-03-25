from django.contrib import admin

from .models import UploadAsset


@admin.register(UploadAsset)
class UploadAssetAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description", "owner__username")
