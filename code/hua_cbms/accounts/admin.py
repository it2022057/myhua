from django.contrib import admin

from accounts.models import StaffMember, PersonalInfo, CustomUserPermissions

# Register your models here.

admin.site.register(StaffMember)
admin.site.register(CustomUserPermissions)
admin.site.register(PersonalInfo)