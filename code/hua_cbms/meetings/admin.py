from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import AuditModelAdmin
from hua_cbms import settings
from meetings.models import Meeting


# Register your models here.


@admin.register(Meeting)
class MeetingAdmin(AuditModelAdmin):
    list_display = ['index', 'collective_body', 'location', 'when', 'notes', 'present_count', 'absent_count']
    date_hierarchy = 'date_and_time'
    search_fields = ['location', 'collective_body__title_gr', 'collective_body__title_en']
    list_display_links = ['index']
    list_filter = ['collective_body', 'location', 'date_and_time']
    autocomplete_fields = ['collective_body']
    list_select_related = ['collective_body', 'created_by', 'updated_by']
    filter_horizontal = ['present', 'absent']
    ordering = ['collective_body', 'index']
    fieldsets = [
        (_('Στοιχεία Συνεδρίασης'), {
            'fields': ('index', 'collective_body', 'location', 'date_and_time')
        }),
        (_('Παρουσίες'), {
            'fields': ('present', 'absent')
        }),
        (_('Πρόσθετα Στοιχεία'), {
            'fields': ('notes',)
        }),
    ]

    @admin.display(description=_('Ημερομηνία & ώρα'), ordering='date_and_time')
    def when(self, obj):
        if obj.date_and_time:
            return obj.date_and_time.strftime(settings.DATETIME_FORMAT)
        else:
            return '-'

    @admin.display(description=_('Παρών'))
    def present_count(self, obj):
        return obj.present.count()

    @admin.display(description=_('Απών'))
    def absent_count(self, obj):
        return obj.absent.count()
