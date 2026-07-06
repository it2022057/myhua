from dal import autocomplete
from django import forms
from crispy_forms.layout import Layout, Row, Div, Field
from django.utils.translation import gettext_lazy as _

from core.forms import GenericModelForm
from .models import Meeting

MEETING_FIELDS = ['index', 'collective_body', 'location', 'date_and_time', 'notes']

FIELD_LABELS = {
    'index': _('Θέση'),
    'collective_body': _('Συλλογικό Όργανο'),
    'location': _('Τοποθεσία'),
    'date_and_time': _('Ημερομηνία & ώρα'),
    'notes': _('Σημειώσεις')
}

BASE_ATTRS = {
    'data-theme': 'bootstrap-5',
    'data-allow-clear': 'false',
    'class': 'bootstrap5-autocomplete'
}

MEETING_WIDGETS = {
    'collective_body': autocomplete.ModelSelect2(
        url='bodies:collectivebody-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε συλλογικό όργανο')}
    ),
    'notes': forms.Textarea(attrs={'rows': 6})
}


class SecMeetingForm(GenericModelForm):
    scoped_fields = ['collective_body']

    class Meta:
        fields = MEETING_FIELDS
        model = Meeting
        labels = FIELD_LABELS
        widgets = MEETING_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(self.button_element_html,
                css_class="row"),
            Row(
                Div(Field('index'), css_class='col-md-2'),
                Div(Field('collective_body'), css_class='col-md-10'),
                css_class="row"),
            Row(
                Div(Field('location'), css_class='col-md-6'),
                Div(Field('date_and_time'), css_class='col-md-6'),
                css_class="row"),
            Row(
                Div(Field('notes')),
                css_class="row"),
        )
