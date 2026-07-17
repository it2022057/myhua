from django.contrib import admin

from attachments.models import SubjectAttachment, DecisionAttachment

# Register your models here.

admin.site.register(SubjectAttachment)
admin.site.register(DecisionAttachment)