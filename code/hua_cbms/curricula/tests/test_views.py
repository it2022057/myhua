from django.urls import reverse

from core.testing import ProjectTestCase


class CurriculaAutocompleteTests(ProjectTestCase):
    def test_program_autocomplete_is_scoped(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(
            reverse("curricula:program-autocomplete")
        )

        self.assertEqual(response.status_code, 200)
        ids = {int(item["id"]) for item in response.json()["results"]}
        self.assertIn(self.program.pk, ids)
        self.assertNotIn(self.program2.pk, ids)

    def test_department_autocomplete_is_scoped(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(
            reverse("curricula:department-autocomplete")
        )

        self.assertEqual(response.status_code, 200)
        ids = {int(item["id"]) for item in response.json()["results"]}
        self.assertIn(self.department.pk, ids)
        self.assertNotIn(self.department2.pk, ids)

    def test_non_secretariat_cannot_use_program_autocomplete(self):
        self.client.force_login(self.applicant)
        response = self.client.get(
            reverse("curricula:program-autocomplete")
        )
        self.assertEqual(response.status_code, 403)
