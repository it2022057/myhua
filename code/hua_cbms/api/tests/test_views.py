from django.urls import reverse
from rest_framework.test import APIClient

from core.testing import ProjectTestCase


class NextIndexApiTests(ProjectTestCase):
    def setUp(self):
        self.api_client = APIClient()

    def test_secretariat_gets_next_subject_index(self):
        self.api_client.force_login(self.sec_user)
        response = self.api_client.get(
            reverse("api:next_subject_index"),
            {"collective_body_id": self.body.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["next_index"], 2)

    def test_secretariat_gets_next_meeting_index(self):
        self.api_client.force_login(self.sec_user)
        response = self.api_client.get(
            reverse("api:next_meeting_index"),
            {"collective_body_id": self.body.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["next_index"], 2)

    def test_missing_collective_body_parameter_returns_400(self):
        self.api_client.force_login(self.sec_user)
        response = self.api_client.get(reverse("api:next_subject_index"))
        self.assertEqual(response.status_code, 400)

    def test_non_secretariat_cannot_use_next_index_endpoint(self):
        self.api_client.force_login(self.applicant)
        response = self.api_client.get(
            reverse("api:next_subject_index"),
            {"collective_body_id": self.body.pk},
        )
        self.assertEqual(response.status_code, 403)
