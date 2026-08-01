from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.utils import get_lang


# Register your models here.


# Provide common audit functionality for all admin models
class AuditModelAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        # Assign the creator only when the object is first created
        if not change or not obj.created_by_id:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# Provide display fields according to the current language for the admin site
class DisplayFieldAdminMixin:
    # Return the value that matches the current language
    def get_current_language_value(self, obj, greek_field, english_field):
        if get_lang() == 'en':
            return getattr(obj, english_field, None)
        else:
            return getattr(obj, greek_field, None)

    @admin.display(description=_('Τίτλος'), ordering='title_gr')
    def current_title(self, obj):
        return self.get_current_language_value(obj, greek_field='title_gr', english_field='title_en')

    @admin.display(description=_('Ονοματεπώνυμο'), ordering='display_name')
    def current_display_name(self, obj):
        return self.get_current_language_value(obj, greek_field='display_name', english_field='display_name_en')

    @admin.display(description=_('Συντομογραφία'), ordering='short_gr')
    def current_short(self, obj):
        return self.get_current_language_value(obj, greek_field='short_gr', english_field='short_en')

    @admin.display(description=_('Κωδικός'), ordering='code_gr')
    def current_code(self, obj):
        return self.get_current_language_value(obj, greek_field='code_gr', english_field='code_en')
