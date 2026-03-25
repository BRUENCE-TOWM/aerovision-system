from django.urls import path

from .api_views import (
    UploadDetailApiView,
    UploadListApiView,
    UploadYoloAnalyzeApiView,
    YoloInterfaceInfoApiView,
)


urlpatterns = [
    path("uploads/", UploadListApiView.as_view(), name="list_create"),
    path("uploads/<int:pk>/", UploadDetailApiView.as_view(), name="detail"),
    path("uploads/<int:pk>/analyze/", UploadYoloAnalyzeApiView.as_view(), name="analyze"),
    path("yolo/", YoloInterfaceInfoApiView.as_view(), name="yolo_info"),
]
