from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField("显示名称", max_length=100, blank=True)
    title = models.CharField("职位/角色", max_length=120, blank=True)
    organization = models.CharField("所属单位", max_length=120, blank=True)
    bio = models.TextField("个人简介", blank=True)
    contact_email = models.EmailField("联系邮箱", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self) -> str:
        return self.display_name or self.user.get_username()
