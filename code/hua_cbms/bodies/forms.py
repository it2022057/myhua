from crispy_forms.layout import Layout, Row, Div, Field
from dal import autocomplete
from django.utils.translation import gettext_lazy as _

from bodies.models import CollectiveBody
from core.forms import GenericModelForm

COLLECTIVEBODY_FIELDS = ['title_gr', 'title_en', 'participants', 'president', 'secretariat', 'start_date', 'end_date']

FIELD_LABELS = {
    'title_gr': _('Τίτλος (Ελληνικά)'),
    'title_en': _('Τίτλος (Αγγλικά)'),
    'participants': _('Συμμετέχοντες'),
    'president': _('Πρόεδρος'),
    'secretariat': _('Γραμματεία'),
    'start_date': _('Ημερομηνία Έναρξης'),
    'end_date': _('Ημερομηνία Λήξης')
}

BASE_ATTRS = {
    'data-theme': 'bootstrap-5',
    'data-allow-clear': 'false',
    'class': 'bootstrap5-autocomplete'
}

COLLECTIVEBODY_WIDGETS = {
    'participants': autocomplete.ModelSelect2Multiple(
        url='accounts:staff-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε συμμετέχοντες')}
    ),
    'president': autocomplete.ModelSelect2(
        url='accounts:staff-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε πρόεδρο')}
    ),
    'secretariat': autocomplete.ModelSelect2(
        url='accounts:sec-autocomplete',
        attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε γραμματεία')}
    )
}


class SecCollectiveBodyForm(GenericModelForm):
    class Meta:
        fields = COLLECTIVEBODY_FIELDS
        model = CollectiveBody
        labels = FIELD_LABELS
        widgets = COLLECTIVEBODY_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(self.button_element_html,
                css_class="row"),
            Row(
                Div(Field('title_gr'), css_class='col-lg-6'),
                Div(Field('title_en'), css_class='col-lg-6'),
                css_class="row"),
            Row(
                Div(Field('participants')),
                css_class="row"),
            Row(
                Div(Field('president'), css_class='col-md-6'),
                Div(Field('secretariat'), css_class='col-md-6'),
                css_class="row"),
            Row(
                Div(Field('start_date'), css_class='col-md-6'),
                Div(Field('end_date'), css_class='col-md-6'),
                css_class="row"),
        )
