from django.test import TestCase
from django.urls import reverse


class AccountsViewsTest(TestCase):
    def test_login_page(self) -> None:
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self) -> None:
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
