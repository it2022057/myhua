from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class BodiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bodies'
    verbose_name = _('Πανεπιστημιακά Όργανα')
