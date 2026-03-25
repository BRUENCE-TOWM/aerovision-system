from django.conf import settings
from django.db import models


class Announcement(models.Model):
    title = models.CharField("标题", max_length=160)
    summary = models.CharField("摘要", max_length=240, blank=True)
    content = models.TextField("内容")
    is_published = models.BooleanField("发布状态", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "公告"
        verbose_name_plural = "公告"

    def __str__(self) -> str:
        return self.title


class FeedbackEntry(models.Model):
    STATUS_NEW = "new"
    STATUS_REVIEWING = "reviewing"
    STATUS_RESOLVED = "resolved"
    STATUS_CHOICES = [
        (STATUS_NEW, "待处理"),
        (STATUS_REVIEWING, "处理中"),
        (STATUS_RESOLVED, "已完成"),
    ]

    name = models.CharField("姓名", max_length=100)
    email = models.EmailField("邮箱")
    category = models.CharField("类型", max_length=50, default="general")
    message = models.TextField("内容")
    status = models.CharField("处理状态", max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedback_entries",
    )
    created_at = models.DateTimeField("提交时间", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "反馈"
        verbose_name_plural = "反馈"

    def __str__(self) -> str:
        return f"{self.name} - {self.get_status_display()}"
