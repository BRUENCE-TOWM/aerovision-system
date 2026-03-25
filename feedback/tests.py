from django.test import TestCase
from django.urls import reverse


class FeedbackViewsTest(TestCase):
    def test_feedback_create_page(self) -> None:
        response = self.client.get(reverse("feedback:create"))
        self.assertEqual(response.status_code, 200)

    def test_feedback_index_requires_login(self) -> None:
        response = self.client.get(reverse("feedback:index"))
        self.assertEqual(response.status_code, 302)
