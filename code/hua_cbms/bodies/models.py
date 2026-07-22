from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from romanize import romanize

from core.models import TitleStrMixin, TrackedScopedProgramModel
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

    title_gr = models.CharField(max_length=100)
    title_en = models.CharField(null=True, blank=True, max_length=100)
    participants = models.ManyToManyField('accounts.StaffMember', blank=True, related_name='collectivebody_participants')
    president = models.ForeignKey('accounts.StaffMember', null=True, on_delete=models.SET_NULL, related_name='collectivebody_president')
    secretariat = models.ForeignKey('scopes.Secretariat', null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    objects = CollectiveBodyQuery.as_manager()

    def scope_query(self, scope):
        return scope['collective_bodies'].filter(id=self.id).exists()

    def save(self, *args, **kwargs):
        if not (self.title_en and (self.title_en != '')):
            self.title_en = romanize(self.title_gr)

        super().save(*args, update_user=self.updated_by, **kwargs)
