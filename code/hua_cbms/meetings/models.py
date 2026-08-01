from django.core.validators import MinValueValidator
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from django.db import models

from core.models import TrackedModel, TrackedScopedProgramModel
from core.utils import get_ordinal
from hua_cbms import settings
from mailer.gmail import notify
from meetings.emails import MEETING_CREATION_NOTIFICATION_SUBJECT, MEETING_CREATION_NOTIFICATION_BODY, \
    MEETING_UPDATE_NOTIFICATION_SUBJECT, MEETING_UPDATE_NOTIFICATION_BODY, MEETING_CHANGED_BODY_OLD_MEMBERS_SUBJECT, \
    MEETING_CHANGED_BODY_OLD_MEMBERS_BODY, MEETING_CHANGED_BODY_NEW_MEMBERS_SUBJECT
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

    index = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_('Αριθμός Συνεδρίασης'))
    present = models.ManyToManyField('accounts.StaffMember', blank=True, verbose_name=_('Απών'),
                                     related_name='meeting_present')
    absent = models.ManyToManyField('accounts.StaffMember', blank=True, verbose_name=_('Παρών'),
                                    related_name='meeting_absent')
    collective_body = models.ForeignKey('bodies.CollectiveBody', null=True, on_delete=models.CASCADE,
                                        verbose_name=_('Συλλογικό Όργανο'))
    location = models.CharField(max_length=30, default='Ομήρου 9, 17778, Αθήνα, Ελλάδα', verbose_name=_('Τοποθεσία'))
    date_and_time = models.DateTimeField(verbose_name=_('Ημερομηνία & ώρα'))
    notes = models.TextField(null=True, blank=True, verbose_name=_('Σημειώσεις'))

    objects = MeetingQuery.as_manager()

    def __str__(self):
        return _('%s Συνεδρίαση του Συλλογικού Οργάνου %s') % (get_ordinal(self.index), self.collective_body)

    def scope_query(self, scope):
        return scope['collective_bodies'].filter(id=self.collective_body.id).exists()

    # Prepares escaped meeting data for notification message body
    def notification_dict(self):
        return {
            'collective_body_title_gr': escape(self.collective_body.title_gr),
            'collective_body_title_en': escape(self.collective_body.title_en),
            'secretariat_email': escape(self.collective_body.secretariat.user.email),
            'index': escape(self.index),
            'location': escape(self.location),
            'date_and_time': escape(self.date_and_time.strftime(settings.DATETIME_FORMAT)),
            'notes': escape(self.notes),
        }

    # Generates the meeting update notification
    def update_notification(self):
        return MEETING_UPDATE_NOTIFICATION_BODY.format(**self.notification_dict())

    # Generate the meeting creation notification body
    def creation_notification(self):
        return MEETING_CREATION_NOTIFICATION_BODY.format(**self.notification_dict())

    # Notifies the meeting's collective body members (including the president) after meeting creation
    def notify_creation(self):
        emails = (
                self.collective_body.president.email + ', ' +
                ', '.join([staff.email for staff in self.collective_body.participants.all() if staff.email])
        )
        notify.delay(emails, MEETING_CREATION_NOTIFICATION_SUBJECT, self.creation_notification(),
                     cc=settings.DEAN_EMAIL)

    # Notifies the meeting's collective body members (including the president) after meeting update
    def notify_update(self):
        emails = (
                self.collective_body.president.email + ', ' +
                ', '.join([staff.email for staff in self.collective_body.participants.all() if staff.email])
        )
        notify.delay(emails, MEETING_UPDATE_NOTIFICATION_SUBJECT, self.update_notification(), cc=settings.DEAN_EMAIL)

    def notify_collective_body_change(self, old_collective_body, new_collective_body):
        # Retrieve the participants of the previous and current collective bodies
        old_members = old_collective_body.participants.all()
        new_members = new_collective_body.participants.all()

        # Get the actual participant objects affected by the collective body update
        previous_members = old_members.exclude(pk__in=new_members.values_list('pk', flat=True))
        new_members_to_notify = new_members.exclude(pk__in=old_members.values_list('pk', flat=True))

        # Notify participants removed from the meeting's collective body
        emails = ', '.join([member.email for member in previous_members if member.email])
        message_body = MEETING_CHANGED_BODY_OLD_MEMBERS_BODY.format(
            **self.notification_dict(),
            old_collective_body_title_en=escape(old_collective_body.title_en),
            old_collective_body_title_gr=escape(old_collective_body.title_gr),
            old_secretariat_email=escape(old_collective_body.secretariat.user.email),
        )
        notify.delay(emails, MEETING_CHANGED_BODY_OLD_MEMBERS_SUBJECT, message_body)

        # Notify participants added to the new collective body
        emails = ', '.join([member.email for member in new_members_to_notify if member.email])
        notify.delay(emails, MEETING_CHANGED_BODY_NEW_MEMBERS_SUBJECT, self.creation_notification())

    def save(self, *args, **kwargs):
        new = self.id is None
        super().save(*args, update_user=self.updated_by, **kwargs)

        # Send the creation notification only for new meetings
        if new:
            self.notify_creation()
