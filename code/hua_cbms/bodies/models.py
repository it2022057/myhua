from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _
from romanize import romanize

from bodies.emails import UPDATE_NOTIFICATION_BODY, SEC_CREATION_NOTIFICATION_BODY, CREATION_NOTIFICATION_SUBJECT, \
    PRESIDENT_CREATION_NOTIFICATION_BODY, UPDATE_NOTIFICATION_SUBJECT, PARTICIPANT_ADDED_NOTIFICATION_BODY, \
    PARTICIPANT_REMOVED_NOTIFICATION_BODY
from core.models import TitleStrMixin, TrackedScopedProgramModel
from hua_cbms import settings
from mailer.gmail import notify
from scopes.models import ScopedModelPrg, ScopedQueryPrg

User = get_user_model()


# Create your models here.

class CollectiveBodyQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return self.filter(id__in=scope["collective_bodies"])

    # Returns collective bodies that are manually active and have not expired yet
    def active_now(self):
        today = timezone.now()

        return self.filter(active=True, start_date__lte=today, end_date__gte=today)

    # Returns collective bodies that may have the field active=True,
    # because the admin did not manually change it, but their end_date has passed, hence they are expired
    def expired(self):
        today = timezone.now().date()

        return self.filter(end_date__lt=today)

    # Returns collective bodies that are not currently active
    def inactive_now(self):
        today = timezone.now().date()

        return self.exclude(active=True, start_date__lte=today, end_date__gte=today)


class CollectiveBody(TitleStrMixin, TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Συλλογικό Όργανο')
        verbose_name_plural = _('Συλλογικά Όργανα')
        ordering = ['pk']

    title_gr = models.CharField(max_length=100, verbose_name=_('Τίτλος (Ελληνικά)'))
    title_en = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Τίτλος (Αγγλικά)'))
    participants = models.ManyToManyField('accounts.StaffMember', blank=True, verbose_name=_('Συμμετέχοντες'),
                                          related_name='collectivebody_participants')
    president = models.ForeignKey('accounts.StaffMember', null=True, on_delete=models.SET_NULL,
                                  verbose_name=_('Πρόεδρος'), related_name='collectivebody_president')
    secretariat = models.ForeignKey('scopes.Secretariat', null=True, on_delete=models.SET_NULL,
                                    verbose_name=_('Γραμματεία'))
    start_date = models.DateTimeField(verbose_name=_('Ημερομηνία Έναρξης'))
    end_date = models.DateTimeField(verbose_name=_('Ημερομηνία Λήξης'))
    active = models.BooleanField(default=True, verbose_name=_('Ενεργό'))

    objects = CollectiveBodyQuery.as_manager()

    def scope_query(self, scope):
        return scope['collective_bodies'].filter(id=self.id).exists()

    def active_display(self):
        text = 'Yes' if self.active else 'No'
        badge_class = 'bg-success' if self.active else 'bg-danger'

        return format_html('<span class="badge {}" style="font-size: 0.9em">{}</span>', badge_class, text)

    def build_participants_rows(self):
        rows = ''

        # Build the HTML table rows for all collective body participants
        for participant in self.participants.all():
            rows += """
            <tr>
              <td style="border:1px solid #e0e0e0;">{name}</td>
              <td style="border:1px solid #e0e0e0;">{email}</td>
            </tr>
            """.format(name=escape(str(participant)), email=escape(participant.email or '-'))

        # Display an empty row when no participants are assigned
        if not rows:
            rows = """
            <tr>
              <td colspan="2" style="border:1px solid #e0e0e0;">
                -
              </td>
            </tr>
            """

        return rows

    # Prepares escaped collective body data for notification message body
    def notification_dict(self):
        return {
            'title_gr': escape(self.title_gr),
            'title_en': escape(self.title_en),
            'surname_gr': escape(self.president.surname),
            'surname_en': escape(self.president.surname_en),
            'president_display_name_gr': escape(self.president.display_name),
            'president_display_name_en': escape(self.president.display_name_en),
            'secretariat_email': escape(self.secretariat.user.email),
            'start_date': escape(self.start_date.strftime(settings.DATETIME_FORMAT)),
            'end_date': escape(self.end_date.strftime(settings.DATETIME_FORMAT)),
            'active': escape('Ενεργό' if self.active else 'Μη ενεργό'),
            'participants_rows': self.build_participants_rows(),
        }

    # Generates the notification body for a newly added participant
    def participant_added_notification_body(self, url):
        return PARTICIPANT_ADDED_NOTIFICATION_BODY.format(
            **self.notification_dict(),
            url=url,
        )

    # Generates the notification body for a removed participant
    def participant_removed_notification_body(self):
        return PARTICIPANT_REMOVED_NOTIFICATION_BODY.format(**self.notification_dict())

    # Generates the collective body update notification
    def update_notification(self):
        return UPDATE_NOTIFICATION_BODY.format(**self.notification_dict())

    # Generates the creation notification for the secretariat
    def sec_creation_notification(self):
        return SEC_CREATION_NOTIFICATION_BODY.format(**self.notification_dict())

    # Generates the creation notification for the president
    def president_creation_notification(self):
        return PRESIDENT_CREATION_NOTIFICATION_BODY.format(**self.notification_dict())

    # Notifies the secretariat and president after collective body creation
    def notify_creation(self):
        notify.delay(self.secretariat.user.email, CREATION_NOTIFICATION_SUBJECT, self.sec_creation_notification(),
                     cc=settings.ALWAYS_NOTIFY)
        notify.delay(self.president.email, CREATION_NOTIFICATION_SUBJECT, self.president_creation_notification(),
                     cc=settings.ALWAYS_NOTIFY)

    # Notifies the president and participants after an update
    def notify_update(self):
        cc_emails = ', '.join([staff.email for staff in self.participants.all() if staff.email])
        notify.delay(self.president.email, UPDATE_NOTIFICATION_SUBJECT, self.update_notification(), cc=cc_emails)

    def save(self, *args, **kwargs):
        new = self.id is None
        if not (self.title_en and (self.title_en != '')):
            self.title_en = romanize(self.title_gr)

        super().save(*args, update_user=self.updated_by, **kwargs)

        if new:
            self.notify_creation()
        else:
            self.notify_update()
