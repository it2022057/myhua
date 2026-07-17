from crispy_forms.layout import Layout, Row, Div, Field
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from attachments.models import DecisionAttachment, SubjectAttachment
from core.forms import GenericModelForm
from core.widgets import CustomFileInput
from subjects.models import Subject, Decision

ATTACHMENT_FIELDS = ['name', 'file']

FIELD_LABELS = {
    'name': _('Όνομα αρχείου'),
    'file': _('Αρχείο')
}


class BaseAttachmentForm(GenericModelForm):
    def __init__(self, *args, **kwargs):
        self.required_all = True
        super().__init__(*args, **kwargs)

        self.fields['name'].required = False
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Div(Field('name'), css_class='col-md-8'),
                Div(Field('file', template="core/partials/file_input.html"), css_class='col-md-4'),
                css_class='row'
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data['name']
        file = cleaned_data['file']

        if not file:
            self.add_error('file', _('Παρακαλώ επιλέξτε ένα αρχείο'))

        return cleaned_data


class SecSubjectAttachmentForm(BaseAttachmentForm):
    class Meta:
        model = SubjectAttachment
        fields = ATTACHMENT_FIELDS
        labels = FIELD_LABELS
        widgets = {
            'file': CustomFileInput(
                attrs={
                    'accept': '.pdf,.doc,.docx',
                }
            ),
        }

class SecDecisionAttachmentForm(BaseAttachmentForm):
    class Meta:
        model = DecisionAttachment
        fields = ATTACHMENT_FIELDS
        labels = FIELD_LABELS
        widgets = {
            'file': CustomFileInput(
                attrs={
                    'accept': '.pdf,.doc,.docx',
                }
            ),
        }
"""
Create a small formset that can be placed inside the Subject form,
so the secretary can optionally upload attachments connected to that Subject
"""
SubjectAttachmentFormSet = inlineformset_factory(
    Subject,                                # Parent model...Each attachment will belong to one Subject
    SubjectAttachment,                      # Child model that stores the Subject attachments
    form=SecSubjectAttachmentForm,          # Custom form used for every attachment row in the formset
    fields=['name', 'file'],                # Fields to be displayed in each attachment form
    extra=0,                                # No empty attachment form is shown initially
    min_num=0,                              # Attachments are optional (could be 0)
    validate_min=False,                     # Since min_num is 0, this validation is not necessary
    can_delete=True                         # Allows the secretariat to remove attachments in the UpdateView
)

"""
Create a small formset that can be placed inside the Decision form,
so the secretary can optionally upload attachments connected to that Decision
"""
DecisionAttachmentFormSet = inlineformset_factory(
    Decision,                               # Parent model...Each attachment will belong to one Decision
    DecisionAttachment,                     # Child model that stores the Decision attachments
    form=SecDecisionAttachmentForm,         # Custom form used for every attachment row in the formset
    fields=['name', 'file'],                # Fields to be displayed in each attachment form
    extra=0,                                # No empty attachment form is shown initially
    min_num=0,                              # Attachments are optional (could be 0)
    validate_min=False,                     # Since min_num is 0, this validation is not necessary
    can_delete=True                         # Allows the secretariat to remove attachments in the UpdateView
)
