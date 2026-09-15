from api.serializers import MeetingSerializer, StaffSerializer, SubjectSerializer
from core.testing import ProjectTestCase


class SerializerTests(ProjectTestCase):
    def test_staff_serializer_exposes_expected_fields(self):
        data = StaffSerializer(self.participant).data
        self.assertEqual(set(data.keys()), {"email", "given_name", "surname"})

    def test_subject_serializer_exposes_collective_body_id(self):
        data = SubjectSerializer(self.subject).data
        self.assertEqual(data["collective_body_id"], self.body.pk)

    def test_meeting_serializer_exposes_collective_body_id(self):
        data = MeetingSerializer(self.meeting).data
        self.assertEqual(data["collective_body_id"], self.body.pk)
