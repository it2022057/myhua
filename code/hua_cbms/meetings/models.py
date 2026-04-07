from django.utils.translation import  gettext_lazy as _
from django.db import models

from core.models import TrackedModel


# Create your models here.

class Meeting(TrackedModel):
    class Meta:
        verbose_name = _('Συνεδρίαση')
        verbose_name_plural = _('Συνεδριάσεις')

    date_and_time = models.DateTimeField()
    location = models.CharField(max_length=30, default='Ομήρου 9, 17778, Αθήνα, Ελλάδα')
    present = models.ManyToManyField('accounts.StaffMember', blank=True, related_name='meeting_present')
    absent = models.ManyToManyField('accounts.StaffMember', blank=True, related_name='meeting_absent')
    collective_body = models.ForeignKey('bodies.CollectiveBody', null=True, on_delete=models.SET_NULL)
    notes = models.TextField(null=True, blank=True)
    index = models.IntegerField()

