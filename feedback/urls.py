from django.urls import path

from .views import FeedbackCreateView, FeedbackDetailView, FeedbackListView, FeedbackStatusUpdateView


app_name = "feedback"

urlpatterns = [
    path("", FeedbackListView.as_view(), name="index"),
    path("new/", FeedbackCreateView.as_view(), name="create"),
    path("<int:pk>/", FeedbackDetailView.as_view(), name="detail"),
    path("<int:pk>/status/", FeedbackStatusUpdateView.as_view(), name="status"),
]
