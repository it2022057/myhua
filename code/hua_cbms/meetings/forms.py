from crispy_forms.layout import Layout, Row, Div, Field
from dal import autocomplete
from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.checks import validate_meeting_index
from bodies.models import CollectiveBody
from core.forms import GenericModelForm
from subjects.utils import get_last_index
from .models import Meeting

MEETING_FIELDS = ['index', 'present', 'absent', 'collective_body', 'location', 'date_and_time', 'notes']

FIELD_LABELS = {
    'index': _('Αριθμός Συνεδρίασης'),
    'present': _('Παρών'),
    'absent': _('Απών'),
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
    'present': autocomplete.ModelSelect2Multiple(
        url='accounts:participant-autocomplete',
        forward=['collective_body', 'present', 'absent'],
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε τους παρών')}
    ),
    'absent': autocomplete.ModelSelect2Multiple(
        url='accounts:participant-autocomplete',
        forward=['collective_body', 'absent', 'present'],
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε τους απών')}
    ),
    'notes': forms.Textarea(attrs={'rows': 6})
}


class SecMeetingForm(GenericModelForm):
    scoped_fields = ['collective_body', 'present', 'absent']

    class Meta:
        fields = MEETING_FIELDS
        model = Meeting
        labels = FIELD_LABELS
        widgets = MEETING_WIDGETS

    def __init__(self, *args, **kwargs):
        # Get the CollectiveBody's id passed by the create view, if available
        collective_body_id = kwargs.pop('collective_body_id', None)

        super().__init__(*args, **kwargs)

        # If the meeting is being created from a CollectiveBody overview page,
        # automatically select that CollectiveBody in the form
        if collective_body_id:
            collective_body = CollectiveBody.objects.get(pk=collective_body_id)
            self.fields['collective_body'].initial = collective_body

            # Find the highest assigned index for the selected CollectiveBody's meetings
            previous_index = get_last_index(Meeting, collective_body_id=collective_body_id)

            # Set the next available index as the initial value
            self.fields['index'].initial = previous_index + 1

        # If a CreateView is pressed for Meetings, disable present and absent fields
        # because the secretariat updates these fields after the meeting is finished
        if self.instance.pk is None:
            self.disable_form_fields(fields=['present', 'absent'])

        self.helper.layout = Layout(
            Row(self.button_element_html,
                css_class="row"),
            Row(
                Div(Field('index'), css_class='col-md-2'),
                Div(Field('collective_body'), css_class='col-md-10'),
                css_class="row"),
            Row(
                Div(Field('present'), css_class='col-md-6'),
                Div(Field('absent'), css_class='col-md-6'),
                css_class="row"),
            Row(
                Div(Field('location'), css_class='col-md-6'),
                Div(Field('date_and_time'), css_class='col-md-6'),
                css_class="row"),
            Row(
                Div(Field('notes')),
                css_class="row"),
        )

    def clean(self):
        cleaned_data = super().clean()
        index = cleaned_data['index']
        collective_body = cleaned_data['collective_body']

        try:
            validate_meeting_index(index, collective_body, instance=self.instance)
        except forms.ValidationError as e:
            self.add_error('index', e)
