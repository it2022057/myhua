from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from bodyapplications.models import Application
from core.admin import AuditModelAdmin


# Register your models here.


@admin.register(Application)
class ApplicationAdmin(AuditModelAdmin):
    list_display = ['id', 'request_subject', 'description', 'applicant', 'subject', 'created_at', 'created_by']
    date_hierarchy = 'created_at'
    list_display_links = ['id', 'request_subject']
    search_fields = ['request_subject', 'description']
    list_filter = ['subject', 'applicant__username', 'created_by']
    autocomplete_fields = ['applicant', 'subject']
    list_select_related = ['applicant', 'subject']
    fieldsets = [
        (_('Στοιχεία Αίτησης'), {
            'fields': ('request_subject', 'description', 'applicant', 'subject')
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    ]
