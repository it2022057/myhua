from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from bodies.models import CollectiveBody
from core.admin import AuditModelAdmin
from .models import Secretariat


# Register your models here.


@admin.register(Secretariat)
class SecretariatAdmin(AuditModelAdmin):
    readonly_fields = []
    list_display = ['id', 'user__username', 'user__email', 'user__first_name', 'user__last_name', 'program_count',
                    'department_count', 'collective_body_count']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    list_display_links = ['user__username']
    autocomplete_fields = ['user', 'programs', 'departments']
    list_select_related = ['user']
    fieldsets = [
        (_('Βασικά Στοιχεία'), {
            'fields': ['user']
        }),
        (_('Πρόσβαση'), {
            'fields': ['programs', 'departments']
        }),
    ]

    @admin.display(description=_('Προγράμματα Σπουδών'))
    def program_count(self, obj):
        return obj.programs.count()

    @admin.display(description=_('Τμήματα'))
    def department_count(self, obj):
        return obj.departments.count()

    @admin.display(description=_('Συλλογικά Όργανα'))
    def collective_body_count(self, obj):
        return CollectiveBody.objects.filter(secretariat=obj).count()
