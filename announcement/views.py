from django.views.generic import DetailView, ListView

from feedback.models import Announcement


class AnnouncementListView(ListView):
    model = Announcement
    context_object_name = "announcements"
    template_name = "announcement/index.html"
    paginate_by = 10

    def get_queryset(self):
        return Announcement.objects.filter(is_published=True)


class AnnouncementDetailView(DetailView):
    model = Announcement
    context_object_name = "announcement"
    template_name = "announcement/detail.html"

    def get_queryset(self):
        return Announcement.objects.filter(is_published=True)
