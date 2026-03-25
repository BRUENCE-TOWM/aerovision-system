from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from .forms import UploadForm
from .models import UploadAsset


class UploadIndexView(LoginRequiredMixin, ListView):
    model = UploadAsset
    context_object_name = "uploads"
    template_name = "uploads/index.html"
    paginate_by = 8

    def get_queryset(self):
        return UploadAsset.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context["status_counts"] = [
            {"label": "总文件", "value": queryset.count()},
            {"label": "处理中", "value": queryset.filter(status=UploadAsset.STATUS_PROCESSING).count()},
            {"label": "已归档", "value": queryset.filter(status=UploadAsset.STATUS_ARCHIVED).count()},
        ]
        return context


class UploadCreateView(LoginRequiredMixin, FormView):
    form_class = UploadForm
    template_name = "uploads/form.html"
    success_url = reverse_lazy("uploads:index")

    def form_valid(self, form):
        upload = form.save(commit=False)
        upload.owner = self.request.user
        upload.status = UploadAsset.STATUS_UPLOADED
        upload.save()
        messages.success(self.request, "文件已上传并进入管理列表。")
        return super().form_valid(form)


class UploadDetailView(LoginRequiredMixin, DetailView):
    model = UploadAsset
    context_object_name = "upload"
    template_name = "uploads/detail.html"

    def get_queryset(self):
        return UploadAsset.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["api_routes"] = {
            "detail": f"/api/uploads/{self.object.pk}/",
            "analyze": f"/api/uploads/{self.object.pk}/analyze/",
            "uploads": "/api/uploads/",
            "yolo_info": "/api/yolo/",
        }
        context["yolo_default_model"] = getattr(settings, "YOLO_DEFAULT_MODEL", "yolo-placeholder")
        return context
