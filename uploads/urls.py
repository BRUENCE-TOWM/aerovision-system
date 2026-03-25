from django.urls import path

from .views import UploadCreateView, UploadDetailView, UploadIndexView


app_name = "uploads"

urlpatterns = [
    path("", UploadIndexView.as_view(), name="index"),
    path("new/", UploadCreateView.as_view(), name="create"),
    path("<int:pk>/", UploadDetailView.as_view(), name="detail"),
]
