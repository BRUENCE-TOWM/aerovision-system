from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("api/", include("uploads.api_urls")),
    path("accounts/", include("accounts.urls")),
    path("announcements/", include("announcement.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("uploads/", include("uploads.urls")),
    path("feedback/", include("feedback.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
