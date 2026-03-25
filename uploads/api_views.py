from __future__ import annotations

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views import View

from .forms import UploadForm
from .models import UploadAsset
from .services import run_yolo_prediction, serialize_upload


class JsonErrorMixin:
    def json_error(self, message: str, status: int = 400) -> JsonResponse:
        return JsonResponse({"ok": False, "error": message}, status=status)


class UploadListApiView(LoginRequiredMixin, JsonErrorMixin, View):
    def get(self, request: HttpRequest) -> JsonResponse:
        # Upload records are always scoped to the current user.
        uploads = UploadAsset.objects.filter(owner=request.user)
        return JsonResponse(
            {
                "ok": True,
                "items": [serialize_upload(item) for item in uploads],
                "count": uploads.count(),
            }
        )

    def post(self, request: HttpRequest) -> JsonResponse:
        form = UploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)

        # API uploads follow the same ownership and default status rules as the
        # server-rendered upload form.
        upload = form.save(commit=False)
        upload.owner = request.user
        upload.status = UploadAsset.STATUS_UPLOADED
        upload.save()
        return JsonResponse({"ok": True, "item": serialize_upload(upload)}, status=201)


class UploadDetailApiView(LoginRequiredMixin, JsonErrorMixin, View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            upload = UploadAsset.objects.get(pk=pk, owner=request.user)
        except UploadAsset.DoesNotExist:
            return self.json_error("Upload not found.", status=404)

        return JsonResponse({"ok": True, "item": serialize_upload(upload)})


class UploadYoloAnalyzeApiView(LoginRequiredMixin, JsonErrorMixin, View):
    def post(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            upload = UploadAsset.objects.get(pk=pk, owner=request.user)
        except UploadAsset.DoesNotExist:
            return self.json_error("Upload not found.", status=404)

        # The analysis call is synchronous for now so frontend integration can
        # be completed before introducing a background queue.
        upload = run_yolo_prediction(upload)
        return JsonResponse({"ok": True, "item": serialize_upload(upload)})


class YoloInterfaceInfoApiView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> JsonResponse:
        # This endpoint doubles as lightweight API documentation for the
        # frontend and for the future YOLO service handoff.
        return JsonResponse(
            {
                "ok": True,
                "provider": "stub",
                "default_model": getattr(settings, "YOLO_DEFAULT_MODEL", "yolo-placeholder"),
                "supports_sync_predict": True,
                "routes": {
                    "list_uploads": "/api/uploads/",
                    "create_upload": "/api/uploads/",
                    "upload_detail": "/api/uploads/<id>/",
                    "trigger_yolo": "/api/uploads/<id>/analyze/",
                    "yolo_info": "/api/yolo/",
                },
                "request_examples": {
                    "create_upload": {
                        "method": "POST",
                        "content_type": "multipart/form-data",
                        "fields": ["title", "description", "asset"],
                    },
                    "trigger_yolo": {
                        "method": "POST",
                        "content_type": "application/json",
                        "body": {},
                    },
                },
            }
        )
