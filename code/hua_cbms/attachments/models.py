import os

from django.utils.translation import gettext_lazy as _
from django.db import models

from core.models import TrackedModel
from scopes.models import ScopedQueryPrg


# Create your models here.


def subject_attachment_upload_to(instance, filename):
    return os.path.join('attachments', 'subjects', str(instance.subject.pk), filename)


class AttachmentQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return self.all()


class SubjectAttachment(TrackedModel):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Θέματος')
        verbose_name_plural = _('Επισυναπτόμενα Θεμάτων')

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=subject_attachment_upload_to)
    subject = models.ForeignKey('subjects.Subject', null=True, on_delete=models.CASCADE, related_name='attachments')

    objects = AttachmentQuery.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file and not self.name:
            self.name = self.file.name

        super().save(*args, update_user=self.updated_by, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the actual file from MEDIA_ROOT folder
        if self.file:
            self.file.delete(save=False)

        # Delete the database object
        super().delete(*args, **kwargs)


def decision_attachment_upload_to(instance, filename):
    return os.path.join('attachments', 'decisions', str(instance.decision.pk), filename)


class DecisionAttachment(TrackedModel):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Απόφασης')
        verbose_name_plural = _('Επισυναπτόμενα Αποφάσεων')

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=decision_attachment_upload_to)
    decision = models.ForeignKey('subjects.Decision', null=True, on_delete=models.CASCADE, related_name='attachments')

    objects = AttachmentQuery.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file and not self.name:
            self.name = self.file.name

        super().save(*args, update_user=self.updated_by, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the actual file from MEDIA_ROOT folder
        if self.file:
            self.file.delete(save=False)

        # Delete the database object
        super().delete(*args, **kwargs)
