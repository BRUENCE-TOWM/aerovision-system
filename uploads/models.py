from django.conf import settings
from django.db import models


class UploadAsset(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_UPLOADED = "uploaded"
    STATUS_PROCESSING = "processing"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "草稿"),
        (STATUS_UPLOADED, "已上传"),
        (STATUS_PROCESSING, "处理中"),
        (STATUS_ARCHIVED, "已归档"),
    ]

    YOLO_STATUS_IDLE = "idle"
    YOLO_STATUS_QUEUED = "queued"
    YOLO_STATUS_DONE = "done"
    YOLO_STATUS_FAILED = "failed"
    YOLO_STATUS_CHOICES = [
        (YOLO_STATUS_IDLE, "未分析"),
        (YOLO_STATUS_QUEUED, "待分析"),
        (YOLO_STATUS_DONE, "已完成"),
        (YOLO_STATUS_FAILED, "失败"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="upload_assets",
        verbose_name="所属用户",
    )
    title = models.CharField("标题", max_length=160)
    description = models.TextField("描述", blank=True)
    asset = models.FileField("文件", upload_to="assets/%Y/%m/")
    status = models.CharField("状态", max_length=20, choices=STATUS_CHOICES, default=STATUS_UPLOADED)
    yolo_status = models.CharField(
        "YOLO 分析状态",
        max_length=20,
        choices=YOLO_STATUS_CHOICES,
        default=YOLO_STATUS_IDLE,
    )
    yolo_model_name = models.CharField("YOLO 模型名", max_length=100, blank=True)
    yolo_result = models.JSONField("YOLO 结果", null=True, blank=True)
    analyzed_at = models.DateTimeField("分析时间", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "文件资源"
        verbose_name_plural = "文件资源"

    def __str__(self) -> str:
        return self.title
