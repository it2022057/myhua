from meetings.models import Meeting
from core.testing import ProjectTestCase


class MeetingModelTests(ProjectTestCase):
    def test_scope_is_limited_to_secretariat_body(self):
        ids = set(Meeting.objects.sc_filter(user=self.sec_user).values_list("pk", flat=True))
        self.assertIn(self.meeting.pk, ids)
        self.assertNotIn(self.meeting2.pk, ids)

    def test_string_representation_mentions_body(self):
        value = str(self.meeting)
        self.assertIn(str(self.body), value)
