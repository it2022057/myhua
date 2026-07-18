import os

from django import forms
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from accounts.checks import validate_file
from accounts.utils import get_file_hash
from core.models import TrackedModel


# Create your models here.


class AttachmentValidationFormSet(BaseInlineFormSet):
    """
    Checks whether the extra attachment forms have the required file field
    and whether each attachment form uses a different file
    """

    def clean(self):
        super().clean()

        seen_files = {}

        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if self.can_delete and form.cleaned_data.get('DELETE'):
                continue

            file = form.cleaned_data.get('file')

            if form in self.extra_forms:
                try:
                    validate_file(file)
                except forms.ValidationError as e:
                    form.add_error('file', e)

            if not file:
                continue

            file_hash = get_file_hash(file)
            file_size = getattr(file, 'size', None)

            file_key = (file_hash, file_size)

            if file_key in seen_files:
                form.add_error('file', _('Το ίδιο αρχείο έχει ήδη προστεθεί σε άλλο συνημμένο'))

                seen_files[file_key].add_error('file', _('Το ίδιο αρχείο έχει ήδη προστεθεί σε άλλο συνημμένο'))
            else:
                seen_files[file_key] = form


class Attachment(TrackedModel):
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file and not self.name:
            file_name = self.file.name
            name_split = file_name.split('.')
            self.name = name_split[0]

        super().save(*args, update_user=self.updated_by, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the actual file from MEDIA_ROOT folder
        if self.file:
            self.file.delete(save=False)

        # Delete the database object
        super().delete(*args, **kwargs)


def subject_attachment_upload_to(instance, filename):
    return os.path.join('attachments', 'subjects', str(instance.subject.pk), filename)


class SubjectAttachment(Attachment):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Θέματος')
        verbose_name_plural = _('Επισυναπτόμενα Θεμάτων')

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=subject_attachment_upload_to)
    subject = models.ForeignKey('subjects.Subject', null=True, on_delete=models.CASCADE, related_name='attachments')


def decision_attachment_upload_to(instance, filename):
    return os.path.join('attachments', 'decisions', str(instance.decision.pk), filename)


class DecisionAttachment(Attachment):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Απόφασης')
        verbose_name_plural = _('Επισυναπτόμενα Αποφάσεων')

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=decision_attachment_upload_to)
    decision = models.ForeignKey('subjects.Decision', null=True, on_delete=models.CASCADE, related_name='attachments')
