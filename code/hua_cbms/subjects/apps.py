from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class SubjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subjects'
    verbose_name = _('Θέματα και Αποφάσεις')
