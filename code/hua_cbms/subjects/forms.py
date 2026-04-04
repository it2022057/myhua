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

WIDGETS = {
    'type': autocomplete.ModelSelect2(url='subjects:subject-type-autocomplete', attrs={
        'data-placeholder': 'Select type',
        'data-theme': 'bootstrap-5',
        'data-allow-clear': 'false',
        'class': 'bootstrap5-autocomplete'
    }),
    'category': autocomplete.ModelSelect2(url='subjects:subject-category-autocomplete'),
    # 'applicant_user': autocomplete.ModelSelect2(url='accounts:user-autocomplete'),
    # 'program': autocomplete.ModelSelect2(url='curricula:program-autocomplete'),
    # 'department': autocomplete.ModelSelect2(url='curricula:department-autocomplete'),
    # 'school': autocomplete.ModelSelect2(url='curricula:school-autocomplete'),
    # 'collective_body': autocomplete.ModelSelect2(url='bodies:collective-body-autocomplete'),
    'notes': forms.Textarea(attrs={'rows': 4}),
}

class SecSubjectForm(GenericModelForm):
    scoped_fields = ['collective_body']

    class Meta:
        fields = FIELDS
        model = Subject
        labels = FIELD_LABELS
        widgets = WIDGETS
