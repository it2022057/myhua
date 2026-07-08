from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from core.models import TrackedModel, TrackedScopedProgramModel
from scopes.models import ScopedQueryPrg


# Create your models here.

class MeetingQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return self.filter(collective_body__in=scope["collective_bodies"])


class Meeting(TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Συνεδρίαση')
        verbose_name_plural = _('Συνεδριάσεις')
        ordering = ['pk']

    index = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    present = models.ManyToManyField('accounts.StaffMember', blank=True, related_name='meeting_present')
    absent = models.ManyToManyField('accounts.StaffMember', blank=True, related_name='meeting_absent')
    collective_body = models.ForeignKey('bodies.CollectiveBody', null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=30, default='Ομήρου 9, 17778, Αθήνα, Ελλάδα')
    date_and_time = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    objects = MeetingQuery.as_manager()

    def scope_query(self, scope):
        return scope['collective_bodies'].filter(id=self.collective_body.id).exists()

    def save(self, *args, **kwargs):
        super().save(*args, update_user=self.updated_by, **kwargs)

    def is_participant(self, staff_member):
        return self.collective_body.participants.filter(pk=staff_member.pk).exists()

    def has_responded(self, staff_member):
        return (
                self.present.filter(pk=staff_member.pk).exists() or
                self.absent.filter(pk=staff_member.pk).exists()
        )

    def can_respond(self, staff_member):
        return self.is_participant(staff_member) and not self.has_responded(staff_member)
