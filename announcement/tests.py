from django.test import TestCase
from django.urls import reverse


class AnnouncementViewsTest(TestCase):
    def test_announcement_list_page(self) -> None:
        response = self.client.get(reverse("announcement:index"))
        self.assertEqual(response.status_code, 200)
