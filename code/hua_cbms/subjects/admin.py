from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _, ngettext

from core.admin import DisplayFieldAdminMixin, AuditModelAdmin
from subjects.models import SubjectCategory, Subject, SubjectType, Decision


# Register your models here.


@admin.register(SubjectType)
class SubjectTypeAdmin(DisplayFieldAdminMixin, AuditModelAdmin):
    list_display = ['id', 'current_title']
    search_fields = ['title_gr', 'title_en']
    list_display_links = ['current_title']
    fieldsets = [
        (_('Βασικά Στοιχεία'), {
            'fields': ('title_gr', 'title_en')
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    ]


@admin.register(SubjectCategory)
class SubjectCategoryAdmin(SubjectTypeAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(AuditModelAdmin):
    list_display = ['index', 'type', 'category', 'applicant_user', 'program', 'department', 'collective_body', 'notes']
    search_fields = ['type__title_gr', 'type__title_en', 'category__title_gr', 'category__title_en']
    list_filter = ['type', 'category', 'program', 'department', 'school', 'collective_body']
    autocomplete_fields = ['type', 'category', 'applicant_user', 'program', 'department', 'school', 'collective_body']
    list_select_related = ['type', 'category', 'applicant_user', 'program', 'department', 'school', 'collective_body',
                           'created_by', 'updated_by']
    ordering = ['collective_body', 'index']
    fieldsets = [
        (_('Στοιχεία Θέματος'), {
            'fields': (('index',), ('type', 'category'), 'applicant_user', 'collective_body')
        }),
        (_('Ακαδημαϊκά Στοιχεία'), {
            'fields': ('program', 'department', 'school')
        }),
        (_('Πρόσθετα Στοιχεία'), {
            'fields': ('notes',)
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    ]


@admin.register(Decision)
class DecisionAdmin(AuditModelAdmin):
    list_display = ['id', 'subject', 'decision_title']
    search_fields = ['title', 'subject__type__title_gr', 'subject__type__title_en', 'subject__category__title_gr',
                     'subject__category__title_en']
    list_filter = ['title']
    autocomplete_fields = ['subject']
    list_select_related = ['subject', 'created_by', 'updated_by']
    ordering = ['subject']
    fieldsets = [
        (_('Στοιχεία Απόφασης'), {
            'fields': ('title', 'subject')
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    ]
    actions = ['set_approval', 'set_rejection', 'set_pending']

    @admin.display(description=_('Τελική Απόφαση'), ordering='title')
    def decision_title(self, obj):
        return obj.get_title_display()

    @admin.action(description=_('Ορισμός ως έγκριση'))
    def set_approval(self, request, queryset):
        updated = queryset.update(title=Decision.TITLE_APPROVAL)
        self.message_user(
            request,
            ngettext(
                'Ορίστηκε ως έγκριση %d Απόφαση.',
                'Ορίστηκαν ως έγκριση %d Αποφάσεις.',
                updated,
            ) % updated,
            messages.SUCCESS
        )

    @admin.action(description=_('Ορισμός ως απόρριψη'))
    def set_rejection(self, request, queryset):
        updated = queryset.update(title=Decision.TITLE_REJECTION)
        self.message_user(
            request,
            ngettext(
                'Ορίστηκε ως απόρριψη %d Απόφαση.',
                'Ορίστηκαν ως απόρριψη %d Αποφάσεις.',
                updated,
            ) % updated,
            messages.SUCCESS
        )

    @admin.action(description=_('Ορισμός ως σε εκκρεμότητα'))
    def set_pending(self, request, queryset):
        updated = queryset.update(title=Decision.TITLE_PENDING)
        self.message_user(
            request,
            ngettext(
                'Ορίστηκε ως εκκρεμότητα %d Απόφαση.',
                'Ορίστηκαν ως εκκρεμότητα %d Αποφάσεις.',
                updated,
            ) % updated,
            messages.SUCCESS
        )
