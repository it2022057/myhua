from core.models import get_latest_or_create, get_or_create_object
from core.testing import ProjectTestCase
from subjects.models import SubjectType


class TrackedModelTests(ProjectTestCase):
    def test_tracked_model_sets_create_and_update_metadata(self):
        obj = SubjectType(
            title_gr="Tracked",
            title_en="Tracked",
            updated_by=self.sec_user,
        )
        obj.save()

        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)
        self.assertEqual(obj.created_by, self.sec_user)
        self.assertEqual(obj.updated_by, self.sec_user)

        created_at = obj.created_at
        obj.title_gr = "Tracked changed"
        obj.updated_by = self.admin
        obj.save()

        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_by, self.admin)
