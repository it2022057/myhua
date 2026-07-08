from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from romanize import romanize

from core.models import TitleStrMixin, TrackedScopedProgramModel, TrackedModel
from curricula.models import Department
from scopes.models import ScopedQueryPrg, ScopedModelPrg

User = get_user_model()
# Create your models here.


class SubjectTypeQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return SubjectType.objects.all()


class SubjectType(TitleStrMixin, TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Τύπος Θέματος')
        verbose_name_plural = _('Τύποι Θεμάτων')
        ordering = ['pk']

    title_gr = models.CharField(max_length=100)
    title_en = models.CharField(null = True, blank = True, max_length=100)

    objects = SubjectTypeQuery.as_manager()

    def scope_query(self, scope):
        return True

    def save(self, *args, **kwargs):
        if not (self.title_en and (self.title_en != '')):
            self.title_en = romanize(self.title_gr)

        super().save(*args, update_user = self.updated_by, **kwargs)


class SubjectCategoryQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return SubjectCategory.objects.all()


class SubjectCategory(TitleStrMixin, TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Κατηγορία Θέματος')
        verbose_name_plural = _('Κατηγορίες Θεμάτων')
        ordering = ['pk']

    title_gr = models.CharField(max_length=100)
    title_en = models.CharField(null = True, blank = True, max_length=100)

    objects = SubjectCategoryQuery.as_manager()

    def scope_query(self, scope):
        return True

    def save(self, *args, **kwargs):
        if not (self.title_en and (self.title_en != '')):
            self.title_en = romanize(self.title_gr)

        super().save(*args, update_user = self.updated_by,  **kwargs)


class SubjectQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return self.filter(collective_body__in=scope["collective_bodies"])


class Subject(TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Θέμα')
        verbose_name_plural = _('Θέματα')
        ordering = ['pk']

    index = models.PositiveIntegerField(validators=[MinValueValidator(1)])
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

    def save(self, *args, **kwargs):
        super().save(*args, update_user = self.updated_by,  **kwargs)


class DecisionQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return self.filter(subject__collective_body__in=scope["collective_bodies"])


class Decision(TitleStrMixin, TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Απόφαση')
        verbose_name_plural = _('Αποφάσεις')
        ordering = ['pk']

    title_gr = models.CharField(max_length=100)
    title_en = models.CharField(null = True, blank = True, max_length=100)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)

    objects = DecisionQuery.as_manager()

    def scope_query(self, scope):
        return scope['collective_bodies'].filter(id=self.subject.collective_body.id).exists()

    def save(self, *args, **kwargs):
        if not (self.title_en and (self.title_en != '')):
            self.title_en = romanize(self.title_gr)

        super().save(*args, update_user = self.updated_by, **kwargs)

