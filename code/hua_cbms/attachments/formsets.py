from django.forms import inlineformset_factory

from attachments.models import SubjectAttachment, AttachmentValidationFormSet, DecisionAttachment, ApplicationAttachment
from bodyapplications.models import Application
from subjects.models import Subject, Decision
from .forms import SecSubjectAttachmentForm, SecDecisionAttachmentForm, SecApplicationAttachmentForm, ApplicantApplicationAttachmentForm

"""
Create a small formset that can be placed inside the Subject form,
so the secretary can optionally upload attachments connected to that Subject
"""

SubjectAttachmentFormSet = inlineformset_factory(
    Subject,  # Parent model...Each attachment will belong to one Subject
    SubjectAttachment,  # Child model that stores the Subject attachments
    form=SecSubjectAttachmentForm,  # Custom form used for every attachment row in the formset
    formset=AttachmentValidationFormSet,  # Custom validation for all attachment forms that works at the formset level
    fields=['name', 'file'],  # Fields to be displayed in each attachment form
    extra=0,  # No empty attachment form is shown initially
    min_num=0,  # Attachments are optional (could be 0)
    validate_min=False,  # Since min_num is 0, this validation is not necessary
    can_delete=True  # Allows the secretariat to remove attachments in the UpdateView
)

"""
Create a small formset that can be placed inside the Decision form,
so the secretary can optionally upload attachments connected to that Decision
"""

DecisionAttachmentFormSet = inlineformset_factory(
    Decision,  # Parent model...Each attachment will belong to one Decision
    DecisionAttachment,  # Child model that stores the Decision attachments
    form=SecDecisionAttachmentForm,  # Custom form used for every attachment row in the formset
    formset=AttachmentValidationFormSet,  # Custom validation for all attachment forms that works at the formset level
    fields=['name', 'file'],  # Fields to be displayed in each attachment form
    extra=0,  # No empty attachment form is shown initially
    min_num=0,  # Attachments are optional (could be 0)
    validate_min=False,  # Since min_num is 0, this validation is not necessary
    can_delete=True  # Allows the secretariat to remove attachments in the UpdateView
)

"""
Create a small formset that can be placed inside the Application form, so the secretariat can see the attachments 
connected to that Application, but disabled because he cannot change them
"""

SecApplicationAttachmentFormSet = inlineformset_factory(
    Application,  # Parent model...Each attachment will belong to one Application
    ApplicationAttachment,  # Child model that stores the Application attachments
    form=SecApplicationAttachmentForm,  # Custom form used for every attachment row in the formset
    formset=AttachmentValidationFormSet,  # Custom validation for all attachment forms that works at the formset level
    fields=['name', 'file'],  # Fields to be displayed in each attachment form
    extra=0,  # No empty attachment form is shown initially
    min_num=0,  # Attachments are optional (could be 0)
    validate_min=False,  # Since min_num is 0, this validation is not necessary
    can_delete=False  # Forbids the secretariat to remove attachments in the UpdateView
)

"""
Create a small formset that can be placed inside the Application form,
so the applicant can optionally upload attachments connected to that Application
"""

ApplicantApplicationAttachmentFormSet = inlineformset_factory(
    Application,  # Parent model...Each attachment will belong to one Application
    ApplicationAttachment,  # Child model that stores the Application attachments
    form=ApplicantApplicationAttachmentForm,  # Custom form used for every attachment row in the formset
    formset=AttachmentValidationFormSet,  # Custom validation for all attachment forms that works at the formset level
    fields=['name', 'file'],  # Fields to be displayed in each attachment form
    extra=0,  # No empty attachment form is shown initially
    min_num=0,  # Attachments are optional (could be 0)
    validate_min=False,  # Since min_num is 0, this validation is not necessary
    can_delete=True  # Allows the applicant to remove attachments in the UpdateView
)
