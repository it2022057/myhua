from datetime import timedelta

from django.urls import reverse

from core.testing import ProjectTestCase


class MeetingViewTests(ProjectTestCase):
    def test_secretariat_list_hides_past_meetings(self):
        past = self.make_meeting(
            collective_body=self.body,
            index=2,
            date_and_time=self.now - timedelta(days=2),
        )

        self.client.force_login(self.sec_user)
        response = self.client.get(
            reverse("meetings:sec_list_meetings")
        )

        ids = set(response.context["objects"].values_list("pk", flat=True))
        self.assertIn(self.meeting.pk, ids)
        self.assertNotIn(past.pk, ids)

    def test_admin_list_includes_past_meetings(self):
        past = self.make_meeting(
            collective_body=self.body,
            index=2,
            date_and_time=self.now - timedelta(days=2),
        )

        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("meetings:sec_list_meetings")
        )

        ids = set(response.context["objects"].values_list("pk", flat=True))
        self.assertIn(past.pk, ids)

    def test_staff_list_shows_only_active_body_participated_meetings(self):
        self.client.force_login(self.participant.user)
        response = self.client.get(
            reverse("meetings:staff_list_meetings")
        )

        ids = set(response.context["objects"].values_list("pk", flat=True))
        self.assertIn(self.meeting.pk, ids)
        self.assertNotIn(self.meeting2.pk, ids)
