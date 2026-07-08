from dal import autocomplete
from django import forms
from crispy_forms.layout import Layout, Row, Div, Field, HTML
from django.utils.translation import gettext_lazy as _

from accounts.checks import validate_subject_index
from core.forms import GenericModelForm
from subjects.models import Subject, Decision, SubjectType, SubjectCategory

SUBJECT_FIELDS = ['index', 'type', 'category', 'applicant_user', 'program', 'department', 'school', 'collective_body', 'notes']

DECISION_FIELDS = ['title_gr', 'title_en', 'subject']

SUBJECT_TYPE_FIELDS = ['title_gr', 'title_en']

FIELD_LABELS = {
    'index': _('Θέση'),
    'type': _('Τύπος'),
    'category': _('Κατηγορία'),
    'applicant_user': _('Αιτών'),
    'program': _('Πρόγραμμα Σπουδών'),
    'department': _('Τμήμα'),
    'school': _('Σχολή'),
    'collective_body': _('Συλλογικό Όργανο'),
    'notes': _('Σημειώσεις'),

    'title_gr': _('Τίτλος (Ελληνικά)'),
    'title_en': _('Τίτλος (Αγγλικά)'),
    'subject': _('Θέμα')
}

BASE_ATTRS = {
    'data-theme': 'bootstrap-5',
    'data-allow-clear': 'false',
    'class': 'bootstrap5-autocomplete'
}

SUBJECT_WIDGETS = {
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
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε αιτών')}
    ),
    'program': autocomplete.ModelSelect2(
        url='curricula:program-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε πρόγραμμα σπουδών')}
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
    'notes': forms.Textarea(attrs={'rows': 6})
}

DECISION_WIDGETS = {
    'subject': autocomplete.ModelSelect2(
        url='subjects:subject-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε θέμα')}
    )
}


class SecSubjectForm(GenericModelForm):
    scoped_fields = ['collective_body']

    class Meta:
        fields = SUBJECT_FIELDS
        model = Subject
        labels = FIELD_LABELS
        widgets = SUBJECT_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(self.button_element_html,
                css_class="row"),
            Row(
                Div(Field('index'), css_class='col-md-2'),
                Div(Field('type'), css_class='col-md-5'),
                Div(Field('category'), css_class='col-md-5'),
                css_class="row"),
            Row(
                Div(Field('applicant_user')),
                css_class="row"),
            Row(
                Div(Field('program'), css_class='col-md-4'),
                Div(Field('department'), css_class='col-md-4'),
                Div(Field('school'), css_class='col-md-4'),
                css_class="row"),
            Row(
                Div(Field('collective_body')),
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
            validate_subject_index(index, collective_body, instance=self.instance)
        except forms.ValidationError as e:
            self.add_error('index', e)


class SecSubjectTypeForm(GenericModelForm):
    class Meta:
        fields = SUBJECT_TYPE_FIELDS
        model = SubjectType
        labels = FIELD_LABELS


class SecSubjectCategoryForm(GenericModelForm):
    class Meta:
        fields = SUBJECT_TYPE_FIELDS
        model = SubjectCategory
        labels = FIELD_LABELS


class SecDecisionForm(GenericModelForm):
    scoped_fields = ['subject']

    class Meta:
        fields = DECISION_FIELDS
        model = Decision
        labels = FIELD_LABELS
        widgets = DECISION_WIDGETS
