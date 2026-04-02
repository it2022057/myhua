from django.contrib import admin

from attachments.models import Attachment, DecisionAttachment

# Register your models here.

admin.site.register(Attachment)
admin.site.register(DecisionAttachment)