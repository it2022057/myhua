from django import forms
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from accounts.checks import validate_file
from accounts.directories import subject_attachment_dir, decision_attachment_dir, application_attachment_dir
from accounts.utils import get_file_hash
from core.models import TrackedModel


# Create your models here.


class AttachmentValidationFormSet(BaseInlineFormSet):
    """
    Checks whether the extra attachment forms have the required file field
    and whether each attachment form uses a different file
    """

    def clean(self):
        # Apply the default formset validation
        super().clean()

        # Variable that stores uploaded files by their hash and size
        seen_files = {}

        for form in self.forms:
            # Skip forms that were not cleaned successfully
            if not hasattr(form, 'cleaned_data'):
                continue

            # Ignore forms marked for deletion
            if self.can_delete and form.cleaned_data.get('DELETE'):
                continue

            file = form.cleaned_data.get('file')

            # Require a valid file in newly added attachment forms
            if form in self.extra_forms:
                try:
                    validate_file(file)
                except forms.ValidationError as e:
                    form.add_error('file', e)

            # Skip next validation when no file is available
            if not file:
                continue

            file_hash = get_file_hash(file)
            file_size = getattr(file, 'size', None)
            # Generate a unique key for the uploaded file, based on its hash and size
            file_key = (file_hash, file_size)

            if file_key in seen_files:
                # Add validation errors to attachment forms that have the same file chosen
                form.add_error('file', _('Το ίδιο αρχείο έχει ήδη προστεθεί σε άλλο συνημμένο'))

                seen_files[file_key].add_error('file', _('Το ίδιο αρχείο έχει ήδη προστεθεί σε άλλο συνημμένο'))
            else:
                # Add the new uploaded file to the selected ones
                seen_files[file_key] = form


class Attachment(TrackedModel):
    class Meta:
        verbose_name = _('Επισυναπτόμενο')
        verbose_name_plural = _('Επισυναπτόμενα')

    name = models.CharField(max_length=100, verbose_name=_('Όνομα Αρχείου'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file and not self.name:
            name_split = self.file.name.split('.')
            self.name = name_split[0]

        super().save(*args, update_user=self.updated_by, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the actual file from MEDIA_ROOT folder
        if self.file:
            self.file.delete(save=False)

        # Delete the database object
        super().delete(*args, **kwargs)

    def download(self):
        if not self.file:
            return ''

        # Generates a download button for the attached file
        return format_html(
            '<a href="{}" class="btn btn-secondary mb-2 download">'
            '<span class="mto">download</span> '
            '<em>{}</em>'
            '</a>',

            reverse('media_download', kwargs={'path': self.file.name}), self.name
        )


class SubjectAttachment(Attachment):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Θέματος')
        verbose_name_plural = _('Επισυναπτόμενα Θεμάτων')

    file = models.FileField(upload_to=subject_attachment_dir, verbose_name=_('Αρχείο'))
    subject = models.ForeignKey('subjects.Subject', null=True, on_delete=models.CASCADE, verbose_name=_('Θέμα'),
                                related_name='attachments')


class DecisionAttachment(Attachment):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Απόφασης')
        verbose_name_plural = _('Επισυναπτόμενα Αποφάσεων')

    file = models.FileField(upload_to=decision_attachment_dir)
    decision = models.ForeignKey('subjects.Decision', null=True, on_delete=models.CASCADE, verbose_name=_('Απόφαση'),
                                 related_name='attachments')


class ApplicationAttachment(Attachment):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Αίτησης')
        verbose_name_plural = _('Επισυναπτόμενα Αιτήσεων')

    file = models.FileField(upload_to=application_attachment_dir)
    application = models.ForeignKey('bodyapplications.Application', null=True, on_delete=models.CASCADE,
                                    verbose_name=_('Αίτηση'), related_name='attachments')
