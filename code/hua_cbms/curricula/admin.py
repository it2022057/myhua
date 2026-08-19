from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _, ngettext

from core.admin import AuditModelAdmin, DisplayFieldAdminMixin
from .models import School, Department, StudyProgram, Institution


# Register your models here.


@admin.register(Institution)
class InstitutionAdmin(DisplayFieldAdminMixin, AuditModelAdmin):
    readonly_fields = []
    list_display = ['id', 'current_title', 'current_short', 'current_code']
    list_display_links = ['current_title']
    search_fields = ['title_gr', 'title_en', 'short_gr', 'short_en']
    fieldsets = [
        (_('Στοιχεία Ιδρύματος'), {
            'fields': ('title_gr', 'title_en', 'short_gr', 'short_en', 'code_gr', 'code_en')
        }),
    ]


@admin.register(School)
class SchoolAdmin(DisplayFieldAdminMixin, AuditModelAdmin):
    readonly_fields = []
    list_display = ['id', 'current_title', 'current_short', 'current_code', 'institution']
    list_display_links = ['current_title']
    search_fields = ['title_gr', 'title_en', 'short_gr', 'short_en']
    list_filter = ['institution']
    autocomplete_fields = ['institution']
    list_select_related = ['institution']
    fieldsets = [
        (_('Στοιχεία Σχολής'), {
            'fields': ('title_gr', 'title_en', 'short_gr', 'short_en', 'code_gr', 'code_en', 'institution')
        }),
    ]


@admin.register(Department)
class DepartmentAdmin(DisplayFieldAdminMixin, AuditModelAdmin):
    readonly_fields = []
    list_display = ['id', 'current_title', 'current_short', 'current_code', 'institution', 'school']
    list_display_links = ['current_title']
    search_fields = ['title_gr', 'title_en', 'short_gr', 'short_en']
    list_filter = ['school', 'school__institution']
    autocomplete_fields = ['school']
    list_select_related = ['school', 'school__institution']
    fieldsets = [
        (_('Στοιχεία Τμήματος'), {
            'fields': ('title_gr', 'title_en', 'short_gr', 'short_en', 'code_gr', 'code_en', 'school')
        }),
    ]
    
    @admin.display(description=_('Ίδρυμα'), ordering='school__institution')
    def institution(self, obj):
        if obj.school:
            return obj.school.institution
        return None


@admin.register(StudyProgram)
class StudyProgramAdmin(DisplayFieldAdminMixin, AuditModelAdmin):
    readonly_fields = []
    list_display = ['id', 'current_title', 'current_short', 'current_code', 'sis_code', 'department', 'type', 'active']
    list_display_links = ['current_title']
    list_editable = ['active']
    search_fields = ['title_gr', 'title_en', 'short_gr', 'short_en', 'sis_code']
    list_filter = ['department', 'department__school__institution', 'department__school', 'type', 'active',
                   'has_thesis', 'thesis_semesters', 'thesis_has_report', 'thesis_report_semesters']
    autocomplete_fields = ['department']
    list_select_related = ['department', 'department__school', 'department__school__institution']
    fieldsets = [
        (_('Βασικά Στοιχεία'), {
            'fields': ('title_gr', 'title_en', 'short_gr', 'short_en', 'code_gr', 'code_en')
        }),
        (_('Ακαδημαϊκά Στοιχεία'), {
            'fields': ('department', 'type', 'sis_code', 'active')
        }),
        (_('Διπλωματική Εργασία'), {
            'fields': ('has_thesis', 'thesis_semesters', 'thesis_has_report', 'thesis_report_semesters')
        }),
    ]
    actions = ['mark_as_active', 'mark_as_inactive', 'set_has_thesis', 'unset_has_thesis', 'set_thesis_has_report',
               'unset_thesis_has_report']

    @admin.action(description=_('Ορισμός ως ενεργού'))
    def mark_as_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(
            request,
            ngettext(
                '%d Πρόγραμμα Σπουδών ορίστηκε ως ενεργό.',
                '%d Προγράμματα Σπουδών ορίστηκαν ως ενεργά.',
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
                '%d Πρόγραμμα Σπουδών ορίστηκε ως μη ενεργό.',
                '%d Προγράμματα Σπουδών ορίστηκαν ως μη ενεργά.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Ορισμός ύπαρξης διπλωματικής εργασίας'))
    def set_has_thesis(self, request, queryset):
        updated = queryset.update(has_thesis=True)
        self.message_user(
            request,
            ngettext(
                'Ορίστηκε ύπαρξη διπλωματικής εργασίας σε %d Πρόγραμμα Σπουδών.',
                'Ορίστηκε ύπαρξη διπλωματικής εργασίας σε %d Προγράμματα Σπουδών.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Κατάργηση ύπαρξης διπλωματικής εργασίας'))
    def unset_has_thesis(self, request, queryset):
        updated = queryset.update(has_thesis=False)
        self.message_user(
            request,
            ngettext(
                'Καταργήθηκε η ύπαρξη διπλωματικής εργασίας από %d Πρόγραμμα Σπουδών.',
                'Καταργήθηκε η ύπαρξη διπλωματικής εργασίας από %d Προγράμματα Σπουδών.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Ορισμός ύπαρξης αναφοράς διπλωματικής'))
    def set_thesis_has_report(self, request, queryset):
        updated = queryset.update(thesis_has_report=True)
        self.message_user(
            request,
            ngettext(
                'Ορίστηκε η ύπαρξη αναφοράς διπλωματικής σε %d Πρόγραμμα Σπουδών.',
                'Ορίστηκε η ύπαρξη αναφοράς διπλωματικής σε %d Προγράμματα Σπουδών.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Κατάργηση ύπαρξης αναφοράς διπλωματικής'))
    def unset_thesis_has_report(self, request, queryset):
        updated = queryset.update(thesis_has_report=False)
        self.message_user(
            request,
            ngettext(
                'Καταργήθηκε η ύπαρξη αναφοράς διπλωματικής από %d Πρόγραμμα Σπουδών.',
                'Καταργήθηκε η ύπαρξη αναφοράς διπλωματικής από %d Προγράμματα Σπουδών.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

# admin.site.register(Course)
# admin.site.register(Director)
