import json

from django.urls import reverse

from core.testing import ProjectTestCase


class AccountViewTests(ProjectTestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_applicant_can_open_dashboard(self):
        self.client.force_login(self.applicant)
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_applicant_autocomplete_is_secretariat_only(self):
        self.client.force_login(self.applicant)
        response = self.client.get(reverse("accounts:applicant-autocomplete"))
        self.assertEqual(response.status_code, 403)

    def test_secretariat_can_use_applicant_autocomplete(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(reverse("accounts:applicant-autocomplete"))
        self.assertEqual(response.status_code, 200)

    def test_secretariat_autocomplete_is_superuser_only(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(reverse("accounts:sec-autocomplete"))
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.admin)
        response = self.client.get(reverse("accounts:sec-autocomplete"))
        self.assertEqual(response.status_code, 200)


class ParticipantAutocompleteTests(ProjectTestCase):
    def setUp(self):
        self.client.force_login(self.sec_user)
        self.url = reverse("accounts:participant-autocomplete")

    def _get_results(self, forwarded=None, q=None):
        params = {}

        if forwarded is not None:
            params["forward"] = json.dumps(forwarded)

        if q is not None:
            params["q"] = q

        response = self.client.get(self.url, params)

        self.assertEqual(response.status_code, 200)

        return response.json()["results"]

    def _get_result_ids(self, forwarded=None, q=None):
        results = self._get_results(
            forwarded=forwarded,
            q=q,
        )

        return {
            int(result["id"])
            for result in results
        }

    def test_without_collective_body_returns_no_staff_members(self):
        ids = self._get_result_ids()

        self.assertEqual(ids, set())

    def test_returns_collective_body_participants(self):
        ids = self._get_result_ids(
            forwarded={
                "collective_body": self.body.pk,
            }
        )

        self.assertIn(self.participant.pk, ids)

    def test_returns_collective_body_president(self):
        ids = self._get_result_ids(
            forwarded={
                "collective_body": self.body.pk,
            }
        )

        self.assertIn(self.president.pk, ids)

    def test_does_not_return_staff_from_another_collective_body(self):
        ids = self._get_result_ids(
            forwarded={
                "collective_body": self.body.pk,
            }
        )

        self.assertNotIn(self.other_staff.pk, ids)

    def test_excludes_staff_already_selected_as_present(self):
        ids = self._get_result_ids(
            forwarded={
                "collective_body": self.body.pk,
                "present": [self.participant.pk],
            }
        )

        self.assertNotIn(self.participant.pk, ids)
        self.assertIn(self.president.pk, ids)

    def test_excludes_staff_already_selected_as_absent(self):
        ids = self._get_result_ids(
            forwarded={
                "collective_body": self.body.pk,
                "absent": [self.president.pk],
            }
        )

        self.assertNotIn(self.president.pk, ids)
        self.assertIn(self.participant.pk, ids)

    def test_excludes_present_and_absent_staff_members(self):
        ids = self._get_result_ids(
            forwarded={
                "collective_body": self.body.pk,
                "present": [self.participant.pk],
                "absent": [self.president.pk],
            }
        )

        self.assertNotIn(self.participant.pk, ids)
        self.assertNotIn(self.president.pk, ids)

    def test_search_filters_participants_by_display_name(self):
        ids = self._get_result_ids(
            forwarded={
                "collective_body": self.body.pk,
            },
            q="Participant",
        )

        self.assertIn(self.participant.pk, ids)
        self.assertNotIn(self.president.pk, ids)

    def test_non_secretariat_cannot_use_participant_autocomplete(self):
        self.client.force_login(self.applicant)

        response = self.client.get(
            self.url,
            {
                "forward": json.dumps(
                    {
                        "collective_body": self.body.pk,
                    }
                )
            },
        )

        self.assertEqual(response.status_code, 403)


class StaffMemberAutocompleteTests(ProjectTestCase):
    def setUp(self):
        self.client.force_login(self.sec_user)
        self.url = reverse("accounts:staff-autocomplete")

    def _get_results(self, forwarded=None, q=None):
        params = {}

        if forwarded is not None:
            params["forward"] = json.dumps(forwarded)

        if q is not None:
            params["q"] = q

        response = self.client.get(self.url, params)

        self.assertEqual(response.status_code, 200)

        return response.json()["results"]

    def _get_result_ids(self, forwarded=None, q=None):
        results = self._get_results(
            forwarded=forwarded,
            q=q,
        )

        return {
            int(result["id"])
            for result in results
        }

    def test_returns_staff_members(self):
        ids = self._get_result_ids()

        self.assertIn(self.participant.pk, ids)
        self.assertIn(self.president.pk, ids)
        self.assertNotIn(self.other_staff.pk, ids)

    def test_excludes_selected_participants_when_selecting_president(self):
        ids = self._get_result_ids(
            forwarded={
                "participants": [self.participant.pk],
            }
        )

        self.assertNotIn(self.participant.pk, ids)
        self.assertIn(self.president.pk, ids)

    def test_excludes_selected_president_when_selecting_participants(self):
        ids = self._get_result_ids(
            forwarded={
                "president": self.president.pk,
            }
        )

        self.assertNotIn(self.president.pk, ids)
        self.assertIn(self.participant.pk, ids)

    def test_excludes_both_forwarded_president_and_participants(self):
        ids = self._get_result_ids(
            forwarded={
                "participants": [self.participant.pk],
                "president": self.president.pk,
            }
        )

        self.assertNotIn(self.participant.pk, ids)
        self.assertNotIn(self.president.pk, ids)

    def test_search_filters_staff_members_by_display_name(self):
        ids = self._get_result_ids(q="Participant")

        self.assertIn(self.participant.pk, ids)
        self.assertNotIn(self.president.pk, ids)
        self.assertNotIn(self.other_staff.pk, ids)

    def test_secretariat_can_use_staff_autocomplete(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_superuser_can_use_staff_autocomplete(self):
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_applicant_cannot_use_staff_autocomplete(self):
        self.client.force_login(self.applicant)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
