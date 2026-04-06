from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

from core.models import TitleStrMixin, TrackedScopedProgramModel
from curricula.models import Department
from scopes.models import ScopedQueryPrg, ScopedModelPrg

User = get_user_model()
# Create your models here.

class SubjectType(TitleStrMixin, models.Model):
    class Meta:
        verbose_name = _('Τύπος Θέματος')
        verbose_name_plural = _('Τύποι Θεμάτων')

    title_gr = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)


class SubjectCategory(TitleStrMixin, models.Model):
    class Meta:
        verbose_name = _('Κατηγορία Θέματος')
        verbose_name_plural = _('Κατηγορίες Θεμάτων')

    title_gr = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)


class SubjectQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return self.filter(collective_body__in=scope["collective_bodies"])


class Subject(TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Θέμα')
        verbose_name_plural = _('Θέματα')
        ordering = ['type']

    index = models.IntegerField()
    type = models.ForeignKey(SubjectType, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(SubjectCategory, null=True, blank=True, on_delete=models.CASCADE)
    applicant_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    program = models.ForeignKey('curricula.StudyProgram', null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey('curricula.Department', null=True, on_delete=models.SET_NULL)
    school = models.ForeignKey('curricula.School', null=True, on_delete=models.SET_NULL)
    collective_body = models.ForeignKey('bodies.CollectiveBody', null=True, on_delete=models.SET_NULL)
    notes = models.TextField(null=True, blank=True)

    objects = SubjectQuery.as_manager()

    def scope_query(self, scope):
        return scope['collective_bodies'].filter(id=self.collective_body.id).exists()

    def __str__(self):
        return f"{self.index} - {self.type} - {self.category}"


class Decision(TitleStrMixin, models.Model):
    class Meta:
        verbose_name = _('Απόφαση')
        verbose_name_plural = _('Αποφάσεις')

    title_gr = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)

