from core.testing import ProjectTestCase
from subjects.models import Decision, Subject, SubjectCategory, SubjectType
from subjects.utils import get_last_index


class SubjectModelTests(ProjectTestCase):
    def test_subject_type_generates_english_title_when_missing(self):
        obj = SubjectType.objects.create(
            title_gr="Δοκιμαστικός Τύπος"
        )
        self.assertTrue(obj.title_en)

    def test_subject_category_generates_english_title_when_missing(self):
        obj = SubjectCategory.objects.create(
            title_gr="Δοκιμαστική Κατηγορία"
        )
        self.assertTrue(obj.title_en)

    def test_subject_scope_is_limited_to_body_scope(self):
        ids = set(Subject.objects.sc_filter(user=self.sec_user).values_list("pk", flat=True))
        self.assertIn(self.subject.pk, ids)
        self.assertNotIn(self.subject2.pk, ids)

    def test_decision_scope_is_limited_to_body_scope(self):
        ids = set(Decision.objects.sc_filter(user=self.sec_user).values_list("pk", flat=True))
        self.assertIn(self.decision.pk, ids)
        self.assertNotIn(self.decision2.pk, ids)

    def test_decision_badge_matches_title(self):
        self.assertIn("bg-success", str(self.decision.decision()))

        self.decision.title = Decision.TITLE_REJECTION
        self.assertIn("bg-danger", str(self.decision.decision()))

        self.decision.title = Decision.TITLE_PENDING
        self.assertIn("bg-warning", str(self.decision.decision()))

    def test_get_last_index_returns_highest_index(self):
        Subject.objects.create(
            index=4,
            type=self.subject_type,
            category=self.subject_category,
            collective_body=self.body,
        )
        self.assertEqual(
            get_last_index(
                Subject,
                collective_body_id=self.body.pk,
            ),
            4,
        )
