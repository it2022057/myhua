from django.core.files.uploadedfile import SimpleUploadedFile

from attachments.forms import SecApplicationAttachmentForm
from attachments.formsets import SubjectAttachmentFormSet
from core.testing import ProjectTestCase


class AttachmentFormTests(ProjectTestCase):
    def test_secretariat_application_attachment_form_is_read_only(self):
        form = SecApplicationAttachmentForm(user=self.sec_user)
        self.assertTrue(form.fields["name"].disabled)
        self.assertTrue(form.fields["file"].disabled)

    def test_duplicate_files_in_same_formset_are_rejected(self):
        data = {
            "attachments-TOTAL_FORMS": "2",
            "attachments-INITIAL_FORMS": "0",
            "attachments-MIN_NUM_FORMS": "0",
            "attachments-MAX_NUM_FORMS": "1000",
            "attachments-0-name": "First",
            "attachments-1-name": "Second",
        }
        files = {
            "attachments-0-file": SimpleUploadedFile(
                "one.pdf", b"same-content"
            ),
            "attachments-1-file": SimpleUploadedFile(
                "two.pdf", b"same-content"
            ),
        }
        formset = SubjectAttachmentFormSet(
            data=data,
            files=files,
            instance=self.subject,
            prefix="attachments",
            form_kwargs={"user": self.sec_user},
        )

        self.assertFalse(formset.is_valid())
        self.assertIn("file", formset.forms[0].errors)
        self.assertIn("file", formset.forms[1].errors)

    def test_new_attachment_requires_file(self):
        data = {
            "attachments-TOTAL_FORMS": "1",
            "attachments-INITIAL_FORMS": "0",
            "attachments-MIN_NUM_FORMS": "0",
            "attachments-MAX_NUM_FORMS": "1000",
            "attachments-0-name": "Missing file",
        }
        formset = SubjectAttachmentFormSet(
            data=data,
            files={},
            instance=self.subject,
            prefix="attachments",
            form_kwargs={"user": self.sec_user},
        )

        self.assertFalse(formset.is_valid())
        self.assertIn("file", formset.forms[0].errors)
