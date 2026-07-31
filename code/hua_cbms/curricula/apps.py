from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class CurriculaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'curricula'
    verbose_name = _('Ακαδημαϊκή Δομή')
