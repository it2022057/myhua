from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _, ngettext

from bodies.models import CollectiveBody
from core.admin import AuditModelAdmin, DisplayFieldAdminMixin
from hua_cbms import settings


# Register your models here.


@admin.register(CollectiveBody)
class CollectiveBodyAttachmentAdmin(DisplayFieldAdminMixin, AuditModelAdmin):
    list_display = ['id', 'current_title', 'president', 'secretariat', 'start', 'end', 'active']
    date_hierarchy = 'start_date'
    search_fields = ['title_gr', 'title_en']
    list_editable = ['active']
    list_display_links = ['current_title']
    list_filter = ['president', 'secretariat', 'active', 'start_date', 'end_date']
    autocomplete_fields = ['president', 'secretariat']
    list_select_related = ['president', 'secretariat', 'created_by', 'updated_by']
    filter_horizontal = ['participants']
    fieldsets = [
        (_('Βασικά Στοιχεία'), {
            'fields': ('active', 'title_gr', 'title_en')
        }),
        (_('Σύνθεση'), {
            'fields': ('participants', 'president', 'secretariat')
        }),
        (_('Διάρκεια'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    ]
    actions = ['mark_as_active', 'mark_as_inactive']

    @admin.display(description=_('Ημερομηνία Έναρξης'), ordering='start_date')
    def start(self, obj):
        if obj.start_date:
            return obj.start_date.strftime(settings.DATETIME_FORMAT)
        else:
            return '-'

    @admin.display(description=_('Ημερομηνία Λήξης'), ordering='end_date')
    def end(self, obj):
        if obj.end_date:
            return obj.end_date.strftime(settings.DATETIME_FORMAT)
        else:
            return '-'

    @admin.action(description=_('Ορισμός ως ενεργού'))
    def mark_as_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(
            request,
            ngettext(
                '%d Συλλογικό Όργανο ορίστηκε ως ενεργό.',
                '%d Συλλογικά Όργανα ορίστηκαν ως ενεργά.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Ορισμός ως μη ενεργού'))
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(
            request,
            ngettext(
                '%d Συλλογικό Όργανο ορίστηκε ως μη ενεργό.',
                '%d Συλλογικά Όργανα ορίστηκαν ως μη ενεργά.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )
