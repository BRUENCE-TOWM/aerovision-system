from django.contrib import admin

from .models import Announcement, FeedbackEntry


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "summary", "content")


@admin.register(FeedbackEntry)
class FeedbackEntryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "category", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("name", "email", "message")
