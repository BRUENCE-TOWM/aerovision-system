from django.test import TestCase
from django.urls import reverse


class CoreViewsTest(TestCase):
    def test_home_page(self) -> None:
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self) -> None:
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self) -> None:
        response = self.client.get(reverse("core:contact"))
        self.assertEqual(response.status_code, 200)
