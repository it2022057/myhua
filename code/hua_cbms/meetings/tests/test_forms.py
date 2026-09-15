from datetime import timedelta

from django.utils import timezone

from hua_cbms import settings
from meetings.forms import SecMeetingForm
from core.testing import ProjectTestCase


class MeetingFormTests(ProjectTestCase):
    def test_create_form_disables_attendance_fields(self):
        form = SecMeetingForm(
            user=self.sec_user,
            collective_body_id=self.body.pk,
        )
        self.assertTrue(form.fields["present"].disabled)
        self.assertTrue(form.fields["absent"].disabled)

    def test_create_form_proposes_next_index(self):
        form = SecMeetingForm(
            user=self.sec_user,
            collective_body_id=self.body.pk,
        )
        self.assertEqual(form.fields["index"].initial, 2)
        self.assertEqual(form.fields["collective_body"].initial, self.body)

    def test_duplicate_meeting_index_is_rejected(self):
        data = {
            "index": "1",
            "collective_body": str(self.body.pk),
            "location": "Room B",
            "date_and_time": timezone.localtime(self.now + timedelta(days=5)).strftime("%Y-%m-%d %H:%M"),
            "notes": "Duplicate",
        }
        form = SecMeetingForm(data=data, user=self.sec_user)

        self.assertFalse(form.is_valid())
        self.assertIn("index", form.errors)
