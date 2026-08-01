from crispy_forms.layout import Layout, Row, Div, Field
from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.checks import validate_file
from attachments.models import DecisionAttachment, SubjectAttachment, ApplicationAttachment
from core.forms import GenericModelForm
from core.widgets import CustomFileInput

ATTACHMENT_FIELDS = ['name', 'file']

FIELD_LABELS = {
    'name': _('Όνομα συνημμένου'),
    'file': _('Συνημμένο')
}

ATTACHMENT_WIDGETS = {
    'file': CustomFileInput(
        attrs={
            'accept': '.pdf, .doc, .docx, .png, .jpg, .jpeg, .webp',
        }
    ),
}


class BaseAttachmentForm(GenericModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].required = False
        # Disable the form tag to avoid nested forms and submit attachments together with the main form,
        # either that is a Subject, Decision or Application form
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Div(Field('name'), css_class='col-md-8'),
                Div(Field('file', template="subjects/partials/file_input.html"), css_class='col-md-4'),
                css_class='row'
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data['name']
        file = cleaned_data['file']

        try:
            validate_file(file)
        except forms.ValidationError as e:
            self.add_error('file', e)

        return cleaned_data


class SecSubjectAttachmentForm(BaseAttachmentForm):
    class Meta:
        model = SubjectAttachment
        fields = ATTACHMENT_FIELDS
        labels = FIELD_LABELS
        widgets = ATTACHMENT_WIDGETS


class SecDecisionAttachmentForm(BaseAttachmentForm):
    class Meta:
        model = DecisionAttachment
        fields = ATTACHMENT_FIELDS
        labels = FIELD_LABELS
        widgets = ATTACHMENT_WIDGETS


class SecApplicationAttachmentForm(BaseAttachmentForm):
    disabled_fields = ['name', 'file']

    class Meta:
        model = ApplicationAttachment
        fields = ATTACHMENT_FIELDS
        labels = FIELD_LABELS
        widgets = ATTACHMENT_WIDGETS


class ApplicantApplicationAttachmentForm(BaseAttachmentForm):
    class Meta:
        model = ApplicationAttachment
        fields = ATTACHMENT_FIELDS
        labels = FIELD_LABELS
        widgets = ATTACHMENT_WIDGETS
