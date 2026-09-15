import os
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from attachments.models import SubjectAttachment
from core.testing import ProjectTestCase


class AttachmentModelTests(ProjectTestCase):
    def setUp(self):
        self.media_dir = tempfile.mkdtemp(prefix="myhua-test-media-")
        self.override = override_settings(MEDIA_ROOT=self.media_dir)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media_dir, ignore_errors=True)

    def test_attachment_name_is_generated_from_filename(self):
        attachment = SubjectAttachment.objects.create(
            subject=self.subject,
            file=SimpleUploadedFile("report.pdf", b"pdf-content"),
        )
        self.assertEqual(attachment.name, "report")
        self.assertIn(f"attachments/subjects/{self.subject.pk}/", attachment.file.name)

    def test_delete_removes_database_row_and_physical_file(self):
        attachment = SubjectAttachment.objects.create(
            subject=self.subject,
            file=SimpleUploadedFile("delete.pdf", b"delete-me"),
        )
        file_path = attachment.file.path
        attachment_pk = attachment.pk

        self.assertTrue(os.path.exists(file_path))
        attachment.delete()

        self.assertFalse(os.path.exists(file_path))
        self.assertFalse(SubjectAttachment.objects.filter(pk=attachment_pk).exists())

    def test_download_returns_empty_string_without_file(self):
        attachment = SubjectAttachment(subject=self.subject, name="No file")
        self.assertEqual(attachment.download(), "")
