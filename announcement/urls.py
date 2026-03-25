from django.urls import path

from .views import AnnouncementDetailView, AnnouncementListView


app_name = "announcement"

urlpatterns = [
    path("", AnnouncementListView.as_view(), name="index"),
    path("<int:pk>/", AnnouncementDetailView.as_view(), name="detail"),
]
