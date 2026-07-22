from crispy_forms.layout import Layout, Row, Div, Field
from dal import autocomplete
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Application
from core.forms import GenericModelForm

User = get_user_model()

SEC_APPLICATION_FIELDS = ['request_subject', 'description', 'subject', 'applicant']

APPLICATION_FIELDS = ['request_subject', 'description']

FIELD_LABELS = {
    'request_subject': _('Θέμα Αιτήματος'),
    'description': _('Περιγραφή'),
    'subject': _('Θέμα'),
    'applicant': _('Αιτών')
}

BASE_ATTRS = {
    'data-theme': 'bootstrap-5',
    'data-allow-clear': 'false',
    'class': 'bootstrap5-autocomplete'
}

SEC_APPLICATION_WIDGETS = {
    'subject': autocomplete.ModelSelect2(
        url='subjects:subject-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε θέμα')}
    ),
    'description': forms.Textarea(attrs={'rows': 6})
}


class SecApplicationForm(GenericModelForm):
    scoped_fields = ['subject']
    disabled_fields = ['request_subject', 'description', 'applicant']

    class Meta:
        fields = SEC_APPLICATION_FIELDS
        model = Application
        labels = FIELD_LABELS
        widgets = SEC_APPLICATION_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        applicant = self.instance.applicant
        if applicant:
            self.fields['applicant'].queryset = User.objects.filter(pk=applicant.pk)
            self.fields['applicant'].initial = applicant

        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(self.button_element_html,
                css_class="row"),
            Row(
                Div(Field('request_subject')),
                css_class="row"),
            Row(
                Div(Field('description')),
                css_class="row"),
            Row(
                Div(Field('subject'), css_class='col-md-6'),
                Div(Field('applicant'), css_class='col-md-6'),
                css_class="row"),
        )


class ApplicationForm(GenericModelForm):
    class Meta:
        fields = APPLICATION_FIELDS
        model = Application
        labels = FIELD_LABELS
        widgets = {'description': forms.Textarea(attrs={'rows': 6})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.form_tag = False
