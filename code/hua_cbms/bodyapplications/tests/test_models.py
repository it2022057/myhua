from bodyapplications.models import Application
from core.testing import ProjectTestCase


class ApplicationModelTests(ProjectTestCase):
    def test_pending_application_is_visible_to_secretariat(self):
        scoped = Application.objects.sc_filter(user=self.sec_user)
        self.assertIn(self.pending_application, scoped)

    def test_resolved_application_is_limited_by_body_scope(self):
        scoped = Application.objects.sc_filter(user=self.sec_user)
        self.assertIn(self.resolved_application, scoped)
        self.assertNotIn(self.other_resolved_application, scoped)

    def test_pending_application_scope_query_returns_true(self):
        self.assertTrue(self.pending_application.is_in_scope_of(self.sec_user))

    def test_out_of_scope_resolved_application_returns_false(self):
        self.assertFalse(self.other_resolved_application.is_in_scope_of(self.sec_user))

    def test_string_representation_contains_applicant_and_subject(self):
        value = str(self.pending_application)
        self.assertIn(self.applicant.username, value)
        self.assertIn(self.pending_application.request_subject, value)
