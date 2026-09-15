from django.urls import reverse

from core.testing import ProjectTestCase


class CollectiveBodyViewTests(ProjectTestCase):
    def test_secretariat_list_is_scoped(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(
            reverse("bodies:sec_list_collectivebodies")
        )

        self.assertEqual(response.status_code, 200)
        ids = set(response.context["objects"].values_list("pk", flat=True))
        self.assertIn(self.body.pk, ids)
        self.assertNotIn(self.body2.pk, ids)

    def test_non_admin_cannot_create_collective_body(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(
            reverse("bodies:sec_create_collectivebody")
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_can_open_create_collective_body(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("bodies:sec_create_collectivebody")
        )
        self.assertEqual(response.status_code, 200)

    def test_secretariat_cannot_open_other_secretariat_overview(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(
            reverse(
                "bodies:sec_overview_collectivebody",
                kwargs={"pk": self.body2.pk},
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_applicant_body_list_only_contains_active_bodies(self):
        self.client.force_login(self.applicant)
        response = self.client.get(
            reverse("bodies:applicant_list_collectivebodies")
        )
        self.assertEqual(response.status_code, 200)
