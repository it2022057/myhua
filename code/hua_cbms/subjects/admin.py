from django.contrib import admin

from subjects.models import SubjectCategory, Subject, SubjectType, Decision

# Register your models here.

admin.site.register(SubjectCategory)
admin.site.register(SubjectType)
admin.site.register(Subject)
admin.site.register(Decision)