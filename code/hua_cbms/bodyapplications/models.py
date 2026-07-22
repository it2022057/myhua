from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from core.models import TrackedScopedProgramModel
from scopes.models import ScopedQueryPrg

User = get_user_model()


# Create your models here.


class ApplicationQuery(ScopedQueryPrg):

    def scope_filter(self, scope):
        """
        Secretariats can see all applications that have not yet been linked
        to an official subject, because they are still pending review.

        Once an application is linked to a subject, it is visible only if
        the subject belongs to a collective body inside the secretariat's scope.
        """
        return self.filter(
            Q(subject__isnull=True) |
            Q(subject__collective_body__in=scope['collective_bodies'])
        )



class Application(TrackedScopedProgramModel):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bodyapplications')
    request_subject = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    subject = models.ForeignKey('subjects.Subject', null=True, on_delete=models.SET_NULL, related_name='applications')

    objects = ApplicationQuery.as_manager()

    def scope_query(self, scope):
        # Pending applications are not linked to an official subject yet,
        # so they are visible to all secretariat users
        if not self.subject:
            return True

        if not self.subject.collective_body:
            return False

        # Applications linked to a subject, are visible only when the subject's collective body
        # belongs to the collective bodies available in the secretariat's scope
        return scope['collective_bodies'].filter(pk=self.subject.collective_body.pk).exists()

    def save(self, *args, **kwargs):
        super().save(*args, update_user=self.updated_by, **kwargs)
