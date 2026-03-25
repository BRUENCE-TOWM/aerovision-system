from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import UploadAsset


User = get_user_model()


class UploadViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="tester", password="secret123")

    def test_upload_login_redirect(self) -> None:
        response = self.client.get(reverse("uploads:index"))
        self.assertEqual(response.status_code, 302)

    def test_upload_api_list_requires_login(self) -> None:
        response = self.client.get("/api/uploads/")
        self.assertEqual(response.status_code, 302)

    def test_upload_api_create_and_analyze(self) -> None:
        self.client.login(username="tester", password="secret123")
        upload_file = SimpleUploadedFile("demo.jpg", b"fake-image-content", content_type="image/jpeg")
        create_response = self.client.post(
            "/api/uploads/",
            {
                "title": "Demo Asset",
                "description": "API upload test",
                "asset": upload_file,
            },
        )
        self.assertEqual(create_response.status_code, 201)
        upload_id = create_response.json()["item"]["id"]

        analyze_response = self.client.post(f"/api/uploads/{upload_id}/analyze/")
        self.assertEqual(analyze_response.status_code, 200)
        self.assertEqual(analyze_response.json()["item"]["yolo_status"], UploadAsset.YOLO_STATUS_DONE)
