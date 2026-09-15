from django.urls import reverse

from core.testing import ProjectTestCase


class ApplicationViewTests(ProjectTestCase):
    def test_applicant_list_contains_only_own_applications(self):
        self.client.force_login(self.applicant)
        response = self.client.get(
            reverse("bodyapplications:applicant_list_bodyapplications")
        )

        self.assertEqual(response.status_code, 200)
        ids = set(response.context["objects"].values_list("pk", flat=True))
        self.assertIn(self.pending_application.pk, ids)
        self.assertIn(self.resolved_application.pk, ids)
        self.assertNotIn(self.other_resolved_application.pk, ids)

    def test_secretariat_resolved_list_is_scoped(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(
            reverse("bodyapplications:sec_list_bodyapplications")
        )

        self.assertEqual(response.status_code, 200)
        pending_table = response.context["tables"][0]
        resolved_table = response.context["tables"][1]

        pending_ids = set(pending_table["objects"].values_list("pk", flat=True))
        resolved_ids = set(resolved_table["objects"].values_list("pk", flat=True))

        self.assertIn(self.pending_application.pk, pending_ids)
        self.assertIn(self.resolved_application.pk, resolved_ids)
        self.assertNotIn(self.other_resolved_application.pk, resolved_ids)

    def test_non_secretariat_cannot_open_secretariat_list(self):
        self.client.force_login(self.applicant)
        response = self.client.get(
            reverse("bodyapplications:sec_list_bodyapplications")
        )
        self.assertEqual(response.status_code, 403)
