from dal import autocomplete
from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms import GenericModelForm
from subjects.models import Subject

FIELDS = ['index', 'type', 'category', 'applicant_user', 'program', 'department', 'school', 'collective_body', 'notes']

FIELD_LABELS = {
    'index': _('Δείκτης'),
    'type': _('Τύπος'),
    'category': _('Κατηγορία'),
    'applicant_user': _('Αιτών'),
    'program': _('Πρόγραμμα Σπουδών'),
    'department': _('Τμήμα'),
    'school': _('Σχολή'),
    'collective_body': _('Συλλογικό Όργανο'),
    'notes': _('Σημειώσεις'),
}

BASE_ATTRS = {
    'data-theme': 'bootstrap-5',
    'data-allow-clear': 'false',
    'class': 'bootstrap5-autocomplete'
}

WIDGETS = {
    'type': autocomplete.ModelSelect2(
        url='subjects:subject-type-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε τύπο')}
    ),
    'category': autocomplete.ModelSelect2(
        url='subjects:subject-category-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε κατηγορία')}
    ),
    'applicant_user': autocomplete.ModelSelect2(
        url='accounts:applicant-autocomplete',
        attrs = {**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε αιτών')}
    ),
    'program': autocomplete.ModelSelect2(
        url='curricula:program-autocomplete',
        attrs = {**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε πρόγραμμα σπουδών')}
    ),
    'department': autocomplete.ModelSelect2(
        url='curricula:department-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε τμήμα')}
    ),
    'school': autocomplete.ModelSelect2(
        url='curricula:school-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε σχολή')}
    ),
    'collective_body': autocomplete.ModelSelect2(
        url='bodies:collectivebody-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε συλλογικό όργανο')}
    ),
    'notes': forms.Textarea(attrs={'rows': 4})
}

class SecSubjectForm(GenericModelForm):
    scoped_fields = ['collective_body']

    class Meta:
        fields = FIELDS
        model = Subject
        labels = FIELD_LABELS
        widgets = WIDGETS
