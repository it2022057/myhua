from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from accounts.models import StaffMember, PersonalInfo, CustomUserPermissions

# Register your models here.

class MyAdmin(admin.ModelAdmin):
    admin.site.site_header = _('Διαχείριση HUA')
    admin.site.site_title = _('Ιστότοπος διαχείρισης HUA')


admin.site.register(StaffMember)
admin.site.register(CustomUserPermissions)
admin.site.register(PersonalInfo)