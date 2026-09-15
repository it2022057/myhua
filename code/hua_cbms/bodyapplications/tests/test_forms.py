from bodyapplications.forms import ApplicationForm, SecApplicationForm
from core.testing import ProjectTestCase


class ApplicationFormTests(ProjectTestCase):
    def test_secretariat_cannot_edit_applicant_fields(self):
        form = SecApplicationForm(
            instance=self.resolved_application,
            user=self.sec_user,
        )
        for field in ["request_subject", "description", "applicant"]:
            self.assertTrue(form.fields[field].disabled)
        self.assertFalse(form.fields["subject"].disabled)

    def test_subject_choices_are_scoped(self):
        form = SecApplicationForm(
            instance=self.pending_application,
            user=self.sec_user,
        )
        ids = set(form.fields["subject"].queryset.values_list("pk", flat=True))
        self.assertIn(self.subject.pk, ids)
        self.assertNotIn(self.subject2.pk, ids)

    def test_applicant_form_does_not_expose_subject_link(self):
        form = ApplicationForm(user=self.applicant)
        self.assertEqual(
            set(form.fields.keys()),
            {"request_subject", "description"},
        )
