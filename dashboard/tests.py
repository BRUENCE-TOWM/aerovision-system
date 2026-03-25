from django.test import TestCase
from django.urls import reverse


class DashboardViewsTest(TestCase):
    def test_login_redirect(self) -> None:
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 302)
