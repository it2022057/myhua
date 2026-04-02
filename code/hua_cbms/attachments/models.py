from django.db import models

# Create your models here.

class Attachment(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='templates/')
    subject = models.ForeignKey('subjects.Subject', null=True, on_delete=models.SET_NULL)

class DecisionAttachment(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='templates/')
    decision = models.ForeignKey('subjects.Decision', null=True, on_delete=models.SET_NULL)