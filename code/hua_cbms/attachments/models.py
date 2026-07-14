import os

from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.


def subject_attachment_upload_to(instance, filename):
    return os.path.join('attachments', 'subjects', str(instance.subject.pk), filename)


class SubjectAttachment(models.Model):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Θέματος')
        verbose_name_plural = _('Επισυναπτόμενα Θεμάτων')

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=subject_attachment_upload_to)
    subject = models.ForeignKey('subjects.Subject', null=True, on_delete=models.CASCADE)


def decision_attachment_upload_to(instance, filename):
    return os.path.join('attachments', 'decisions', str(instance.decision.pk), filename)


class DecisionAttachment(models.Model):
    class Meta:
        verbose_name = _('Επισυναπτόμενο Απόφασης')
        verbose_name_plural = _('Επισυναπτόμενα Αποφάσεων')

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=decision_attachment_upload_to)
    decision = models.ForeignKey('subjects.Decision', null=True, on_delete=models.CASCADE)
