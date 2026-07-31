from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meetings'
    verbose_name = _('Συνεδριάσεις')
