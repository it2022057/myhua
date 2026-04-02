from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TitleStrMixin, TrackedScopedProgramModel
from scopes.models import ScopedModelPrg, ScopedQueryPrg

User = get_user_model()
# Create your models here.

class CollectiveBodyQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        return self.filter(id__in=scope["collective_bodies"])


class CollectiveBody(TitleStrMixin, TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Συλλογικό Όργανο')
        verbose_name_plural = _('Συλλογικά Όργανα')

    title_gr = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    participants = models.ManyToManyField('accounts.StaffMember', blank=True, related_name='collectivebody_participants')
    president = models.ForeignKey('accounts.StaffMember', null=True, on_delete=models.SET_NULL, related_name='collectivebody_president')
    secretariat = models.ForeignKey('scopes.Secretariat', null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    objects = CollectiveBodyQuery.as_manager()

    def scope_query(self, scope):
        return scope['collective_bodies'].filter(id=self.id).exists()
