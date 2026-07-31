from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class BodyapplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bodyapplications'
    verbose_name = _('Αιτήσεις προς Πανεπιστημιακά Όργανα')
