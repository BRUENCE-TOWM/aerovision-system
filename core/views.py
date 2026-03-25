from django.views.generic import TemplateView

from feedback.models import Announcement
from uploads.models import UploadAsset


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Keep the landing page data minimal so the homepage stays fast and
        # does not depend on any user-specific query.
        context["featured_announcements"] = Announcement.objects.filter(is_published=True)[:3]
        context["public_stats"] = {
            "announcement_count": Announcement.objects.filter(is_published=True).count(),
            "upload_count": UploadAsset.objects.count(),
        }
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"
