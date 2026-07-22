from django.contrib import admin

from attachments.models import Attachment, SubjectAttachment, DecisionAttachment, ApplicationAttachment

# Register your models here.

admin.site.register(Attachment)
admin.site.register(SubjectAttachment)
admin.site.register(DecisionAttachment)
admin.site.register(ApplicationAttachment)