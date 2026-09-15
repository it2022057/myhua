from core.testing import ProjectTestCase
from subjects.forms import SecDecisionForm, SecSubjectForm


class SubjectFormTests(ProjectTestCase):
    def test_create_form_proposes_next_subject_index(self):
        form = SecSubjectForm(
            user=self.sec_user,
            collective_body_id=self.body.pk,
        )
        self.assertEqual(form.fields["index"].initial, 2)
        self.assertEqual(form.fields["collective_body"].initial, self.body)

    def test_duplicate_subject_index_is_rejected(self):
        data = {
            "index": "1",
            "type": str(self.subject_type.pk),
            "category": str(self.subject_category.pk),
            "applicant_user": str(self.applicant.pk),
            "program": str(self.program.pk),
            "department": str(self.department.pk),
            "school": str(self.school.pk),
            "collective_body": str(self.body.pk),
            "notes": "Duplicate index",
        }
        form = SecSubjectForm(
            data=data,
            user=self.sec_user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("index", form.errors)

    def test_decision_form_can_preselect_subject(self):
        form = SecDecisionForm(
            user=self.sec_user,
            subject_id=self.subject.pk,
        )
        self.assertEqual(form.fields["subject"].initial, self.subject)

    def test_decision_form_contains_placeholder_choice(self):
        form = SecDecisionForm(user=self.sec_user)
        choices = list(form.fields["title"].choices)
        self.assertEqual(choices[0][0], "")
