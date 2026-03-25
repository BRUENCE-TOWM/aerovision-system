from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from feedback.models import Announcement, FeedbackEntry
from uploads.models import UploadAsset


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = {
            "uploads": UploadAsset.objects.filter(owner=self.request.user).count(),
            "feedback": FeedbackEntry.objects.filter(created_by=self.request.user).count(),
            "announcements": Announcement.objects.filter(is_published=True).count(),
        }
        context["recent_uploads"] = UploadAsset.objects.filter(owner=self.request.user)[:5]
        context["recent_announcements"] = Announcement.objects.filter(is_published=True)[:4]
        return context
