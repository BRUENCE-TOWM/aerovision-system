from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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
        queryset = UploadAsset.objects.filter(owner=self.request.user)
        keyword = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()

        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        queryset = UploadAsset.objects.filter(owner=self.request.user)
        context = super().get_context_data(**kwargs)
        context["status_counts"] = [
            {"label": "全部任务", "value": queryset.count()},
            {"label": "处理中", "value": queryset.filter(status=UploadAsset.STATUS_PROCESSING).count()},
            {"label": "已归档", "value": queryset.filter(status=UploadAsset.STATUS_ARCHIVED).count()},
        ]
        context["filter_values"] = {
            "q": self.request.GET.get("q", "").strip(),
            "status": self.request.GET.get("status", "").strip(),
        }
        context["status_choices"] = UploadAsset.STATUS_CHOICES
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
        messages.success(self.request, "识别任务已创建，现已进入任务列表。")
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
