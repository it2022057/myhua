from django.contrib import admin

from attachments.models import SubjectAttachment, DecisionAttachment, Attachment

# Register your models here.

admin.site.register(Attachment)
admin.site.register(SubjectAttachment)
admin.site.register(DecisionAttachment)