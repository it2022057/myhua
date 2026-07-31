import os

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from attachments.models import Attachment, SubjectAttachment, DecisionAttachment, ApplicationAttachment
from core.admin import AuditModelAdmin


# Register your models here.


@admin.display(description=_('Τύπος'))
def file_extension(obj):
    if obj.file:
        return os.path.splitext(obj.file.name)[1].upper().lstrip('.')
    return '-'


@admin.display(description=_('Μέγεθος'))
def file_size(obj):
    if obj.file:
        return f'{obj.file.size / 1024:.1f} KB'
    return '-'


@admin.register(Attachment)
class AttachmentAdmin(AuditModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['name']
    list_display_links = ['name']
    list_filter = ['created_by', 'updated_by']
    list_select_related = ['created_by', 'updated_by']
    fieldsets = [
        (_('Αρχείο'), {
            'fields': ('name',),
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by')
        }),
    ]


@admin.register(SubjectAttachment)
class SubjectAttachmentAdmin(AuditModelAdmin):
    list_display = ['id', 'name', 'subject', 'file', file_size, file_extension, 'created_at', 'created_by']
    date_hierarchy = 'created_at'
    search_fields = ['name', 'subject__type__title_gr', 'subject__type__title_en', 'subject__category__title_gr',
                     'subject__category__title_en', 'file']
    list_display_links = ['name']
    list_filter = ['subject', 'created_by', 'updated_by']
    autocomplete_fields = ['subject']
    list_select_related = ['subject', 'subject__type', 'subject__category', 'created_by', 'updated_by']
    fieldsets = [
        (_('Στοιχεία Αρχείου'), {
            'fields': ('name', 'file', 'subject'),
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    ]


@admin.register(DecisionAttachment)
class DecisionAttachmentAdmin(AuditModelAdmin):
        list_display = ['id', 'name', 'decision', 'file', file_size, file_extension, 'created_at', 'created_by']
        date_hierarchy = 'created_at'
        search_fields = ['name', 'decision__subject__type__title_gr', 'decision__subject__type__title_en',
                         'decision__subject__category__title_gr', 'decision__subject__category__title_en', 'file']
        list_display_links = ['name']
        list_filter = ['decision', 'created_by', 'updated_by']
        autocomplete_fields = ['decision']
        list_select_related = ['decision', 'decision__subject', 'decision__subject__type', 'decision__subject__category'
                               , 'created_by', 'updated_by']
        fieldsets = [
            (_('Στοιχεία Αρχείου'), {
                'fields': ('name', 'file', 'decision'),
            }),
            (_('Σημαντικές Ημερομηνίες'), {
                'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            }),
        ]


@admin.register(ApplicationAttachment)
class ApplicationAttachmentAdmin(AuditModelAdmin):
    list_display = ['id', 'name', 'application', 'file', file_size, file_extension, 'created_at', 'created_by']
    date_hierarchy = 'created_at'
    search_fields = ['name', 'application__request_subject', 'file']
    list_display_links = ['name']
    list_filter = ['application', 'created_by', 'updated_by']
    autocomplete_fields = ['application']
    list_select_related = ['application', 'created_by', 'updated_by']
    fieldsets = [
        (_('Στοιχεία Αρχείου'), {
            'fields': ('name', 'file', 'application'),
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    ]
