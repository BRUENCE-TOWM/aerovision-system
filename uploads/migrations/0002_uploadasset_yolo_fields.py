from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("uploads", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadasset",
            name="analyzed_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="分析时间"),
        ),
        migrations.AddField(
            model_name="uploadasset",
            name="yolo_model_name",
            field=models.CharField(blank=True, max_length=100, verbose_name="YOLO 模型名"),
        ),
        migrations.AddField(
            model_name="uploadasset",
            name="yolo_result",
            field=models.JSONField(blank=True, null=True, verbose_name="YOLO 结果"),
        ),
        migrations.AddField(
            model_name="uploadasset",
            name="yolo_status",
            field=models.CharField(
                choices=[("idle", "未分析"), ("queued", "待分析"), ("done", "已完成"), ("failed", "失败")],
                default="idle",
                max_length=20,
                verbose_name="YOLO 分析状态",
            ),
        ),
    ]
