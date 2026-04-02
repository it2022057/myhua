from django.db import models

# Create your models here.

class Meeting(models.Model):
    date_and_time = models.DateTimeField()
    location = models.CharField(max_length=30, default='Ομήρου 9, 17778, Αθήνα, Ελλάδα')
    present = models.ManyToManyField('accounts.StaffMember', blank=True, related_name='meeting_present')
    absent = models.ManyToManyField('accounts.StaffMember', blank=True, related_name='meeting_absent')
    collective_body = models.ForeignKey('bodies.CollectiveBody', null=True, on_delete=models.SET_NULL)
    notes = models.TextField(null=True, blank=True)
    index = models.IntegerField()

