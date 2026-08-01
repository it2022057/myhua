from crispy_forms.layout import Layout, Row, Div, Field
from dal import autocomplete
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from bodies.models import CollectiveBody
from core.forms import GenericModelForm
from core.widgets import ImageInput
from .checks import validate_password
from .models import StaffMember, PersonalInfo

STAFF_FIELDS = [
    'email', 'given_name', 'surname',
    'institution', 'school', 'department',
    'title', 'is_internal', 'internal_department',
    'can_apply_for_phd', 'can_review_phd_apps', 'can_post_theses'
]

PERSONAL_INFO_FIELDS = [
    'pic', 'given_name', 'surname', 'email', 'secondary_email', 'fathers_name', 'date_of_birth', 'tin', 'ssn', 'gender',
    'department', 'program',
    'mobile_phone', 'home_phone', 'work_phone',
    'home_address_street', 'home_address_no', 'home_address_po_box', 'home_address_city', 'home_address_country',
    'work_address_street', 'work_address_no', 'work_address_po_box', 'work_address_city', 'work_address_country'
]

FIELD_LABELS = {
    'email': _('Ε-mail'),
    'secondary_email': _('2ο E-mail'),
    'given_name': _('Όνομα'),
    'surname': _('Επώνυμο'),
    'institution': _('Ίδρυμα'),
    'school': _('Σχολή'),
    'department': _('Τμήμα'),
    'program': _('Πρόγραμμα Σπουδών'),
    'internal_department': _('Τμήμα εντός του ιδρύματος'),
    'title': _('Ιδιότητα'),
    'is_internal': _('Είναι εσωτερικός;'),
    'can_apply_for_phd': _('Μπορεί να κάνει αίτηση για διδακτορικό;'),
    'can_review_phd_apps': _('Μπορεί να είναι αξιολογητής σε αιτήσεις διδακτορικού;'),
    'can_post_theses': _('Μπορεί να είναι επιβλέπων ή μέλος επιτροπής διπλωματικών;'),
    'pic': _('Εικόνα'),
    'fathers_name': _('Όνομα Πατέρα'), 'date_of_birth': _('Ημ/νία Γέννησης'), 'tin': _('ΑΦΜ'), 'ssn': _('ΑΜΚΑ'), 'gender': _('Φύλο'),
    'mobile_phone': _('Κινητό Τηλέφωνο'), 'home_phone': _('Τηλέφωνο Κατοικίας'), 'work_phone': _('Τηλέφωνο Εργασίας'),
    'home_address_street': _('Οδός Κατοικίας'), 'home_address_no': _('Αριθμός Κατοικίας'),
    'home_address_po_box': _('Τ.Κ. Κατοικίας'), 'home_address_city': _('Πόλη Κατοικίας'),
    'home_address_country': _('Χώρα Κατοικίας'),
    'work_address_street': _('Οδός Εργασίας'), 'work_address_no': _('Αριθμός Εργασίας'),
    'work_address_po_box': _('Τ.Κ. Εργασίας'), 'work_address_city': _('Πόλη Εργασίας'),
    'work_address_country': _('Χώρα Εργασίας')
}

BASE_ATTRS = {
    'data-theme': 'bootstrap-5',
    'data-allow-clear': 'false',
    'class': 'bootstrap5-autocomplete'
}


# Form used in admin site, in order to validate the internal_department field when the is_internal = True
class StaffMemberAdminForm(GenericModelForm):
    class Meta:
        model = StaffMember
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        is_internal = cleaned_data['is_internal']
        internal_department = cleaned_data['internal_department']

        if not is_internal:
            # External staff members must not have internal department
            cleaned_data['internal_department'] = None

        # Optional: if internal staff must always have department
        elif is_internal and not internal_department:
            self.add_error(
                'internal_department',
                _('Το εσωτερικό τμήμα είναι υποχρεωτικό για εσωτερικά μέλη.')
            )

        return cleaned_data


class SecStaffForm(StaffMemberAdminForm):
    scoped_fields = ['internal_department']

    class Meta:
        fields = STAFF_FIELDS
        model = StaffMember
        labels = FIELD_LABELS
        widgets = {'internal_department': autocomplete.ModelSelect2(
            url='curricula:department-autocomplete',
            attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε εσωτερικό τμήμα')}
        )}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(self.button_element_html,
                css_class="row"),
            Row(
                Div(Field('given_name'), css_class='col-md-6'),
                Div(Field('surname'), css_class='col-md-6'),
                css_class="row"),
            Row(
                Div(Field('email')),
                css_class="row"),
            Row(
                Div(Field('is_internal'), css_class='col-md-2'),
                Div(Field('internal_department'), css_class='col-md-5'),
                Div(Field('title'), css_class='col-md-5'),
                css_class="row"),
            Row(
                Div(Field('institution'), css_class='col-md-4'),
                Div(Field('school'), css_class='col-md-4'),
                Div(Field('department'), css_class='col-md-4'),
                css_class="row"),
            Row(
                Div(Field('can_apply_for_phd')),
                css_class="row"),
            Row(
                Div(Field('can_review_phd_apps')),
                css_class="row"),
            Row(
                Div(Field('can_post_theses')),
                css_class="row"),
        )


class SecParticipantsForm(GenericModelForm):
    class Meta:
        fields = ['participants']
        model = CollectiveBody
        labels = { 'participants': _('Συμμετέχοντες') }
        widgets = {
            'participants': autocomplete.ModelSelect2Multiple(
                url='accounts:staff-autocomplete',
                attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε συμμετέχοντες')}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(self.button_element_html,
                css_class="row"),
            Row(
                Div(Field('participants')),
                css_class="row"),
        )


class SecPersonalInfoForm(GenericModelForm):
    scoped_fields = ['department', 'program']

    class Meta:
        fields = PERSONAL_INFO_FIELDS
        model = PersonalInfo
        labels = FIELD_LABELS
        widgets = {
            'department': autocomplete.ModelSelect2(
                url='curricula:department-autocomplete',
                attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε τμήμα')}
            ),
            'program': autocomplete.ModelSelect2(
                url='curricula:program-autocomplete',
                attrs={**BASE_ATTRS, 'data-placeholder': _('Επιλέξτε πρόγραμμα σπουδών')}
            ),
            'pic': ImageInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pass the PersonalInfo instance to the image widget.
        # Used to determine which default profile image to display, when the user has not uploaded a custom picture
        pi = kwargs.get('instance')
        self.fields['pic'].widget.pi = pi

        self.helper.layout = Layout(
            Row(self.button_element_html,
                css_class="row"),
            Row(
                Div(Field('pic'), css_class='col-md-4'),
                Div(Field('given_name'), css_class='col-md-4'),
                Div(Field('surname'), css_class='col-md-4'),
                css_class="row"),
            Row(
                Div(Field('email'), css_class='col-md-6'),
                Div(Field('secondary_email'), css_class='col-md-6'),
                css_class="row"),
            Row(
                Div(Field('gender'), css_class='col-md-2'),
                Div(Field('date_of_birth'), css_class='col-md-3'),
                Div(Field('fathers_name'), css_class='col-md-3'),
                Div(Field('tin'), css_class='col-md-2'),
                Div(Field('ssn'), css_class='col-md-2'),
                css_class="row"),
            Row(
                Div(Field('department'), css_class='col-md-6'),
                Div(Field('program'), css_class='col-md-6'),
                css_class="row"),
            Row(
                Div(Field('mobile_phone'), css_class='col-md-4'),
                Div(Field('home_phone'), css_class='col-md-4'),
                Div(Field('work_phone'), css_class='col-md-4'),
                css_class="row"),
            Row(
                Div(Field('home_address_street'), css_class='col-md-4'),
                Div(Field('home_address_no'), css_class='col-md-2'),
                Div(Field('home_address_po_box'), css_class='col-md-2'),
                Div(Field('home_address_city'), css_class='col-md-2'),
                Div(Field('home_address_country'), css_class='col-md-2'),
                css_class="row"),
            Row(
                Div(Field('work_address_street'), css_class='col-md-4'),
                Div(Field('work_address_no'), css_class='col-md-2'),
                Div(Field('work_address_po_box'), css_class='col-md-2'),
                Div(Field('work_address_city'), css_class='col-md-2'),
                Div(Field('work_address_country'), css_class='col-md-2'),
                css_class="row"),
        )


class SignUpForm(forms.Form):
    email = forms.EmailField(label=_('Το email σας'))
    name = forms.CharField(label=_('To μικρό σας όνομα'), max_length=40)
    surname = forms.CharField(label=_('To επίθετο σας'), max_length=100)
    password1 = forms.CharField(label=_('Κωδικός πρόσβασης'), max_length=100,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(label=_('Κωδικός πρόσβασης (επανάληψη)'), max_length=100,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def __init__(self, *args, **kwargs):
        email = kwargs.pop('email', None)
        super().__init__(*args, **kwargs)
        if email:
            self.fields['email'].disabled = True
            self.fields['email'].initial = email

    def complexity_message(self):
        return _('Παρακαλούμε τηρήστε τις οδηγίες στην οθόνη για τον κωδικό σας!')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        email = cleaned_data['email']

        validate_password(password1, password2)

        if settings.INTERNAL_DOMAIN in email:
            raise forms.ValidationError(
                _('Δεν μπορείτε να χρησιμοποιήσετε διεύθυνση ταχυδρομείου @') + settings.INTERNAL_DOMAIN)

        User = get_user_model()
        users = User.objects.filter(email=email)
        if users.count() > 0:
            raise forms.ValidationError(_('Υπάρχει ήδη χρήστης με αυτό το e-mail'))

        return cleaned_data


class RegisterForm(forms.Form):
    email1 = forms.EmailField(label=_('Το e-mail σας:'))
    email2 = forms.EmailField(label=_('Το e-mail σας (ξανά):'))

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean(self):
        cleaned_data = super().clean()
        if ('email1' not in cleaned_data) or ('email2' not in cleaned_data):
            raise forms.ValidationError(_('Εισάγετε μία έγκυρη διεύθυνση ηλεκτρονικού ταχυδρομείου'))

        email1 = cleaned_data['email1']
        email2 = cleaned_data['email2']

        if email1 != email2:
            raise forms.ValidationError(_('Τα email πρέπει να ταυτίζονται!'))

        if settings.INTERNAL_DOMAIN in email1:
            raise forms.ValidationError(
                _('Αν έχετε ήδη email της μορφής @') + settings.INTERNAL_DOMAIN + _(' δεν χρειάζεται να εγγραφείτε.'))

        User = get_user_model()
        users = User.objects.filter(email=email1)
        if users.count() > 0:
            raise forms.ValidationError(_('Υπάρχει ήδη χρήστης με αυτό το e-mail'))


class ForgotPasswordForm(forms.Form):
    email1 = forms.EmailField(label=_('Το e-mail σας:'))
    email2 = forms.EmailField(label=_('Το e-mail σας (ξανά):'))

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean(self):
        cleaned_data = super().clean()
        if ('email1' not in cleaned_data) or ('email2' not in cleaned_data):
            raise forms.ValidationError(_('Εισάγετε μία έγκυρη διεύθυνση ηλεκτρονικού ταχυδρομείου'))

        email1 = cleaned_data['email1']
        email2 = cleaned_data['email2']

        if email1 != email2:
            raise forms.ValidationError(_('Τα email πρέπει να ταυτίζονται!'))

        if settings.INTERNAL_DOMAIN in email1:
            raise forms.ValidationError(_('Αν έχετε ήδη email της μορφής @') + settings.INTERNAL_DOMAIN + _(
                ' δεν μπορείτε να επαναφέρετε τον κωδικό σας μέσω αυτού του συστήματος.'))

        User = get_user_model()
        users = User.objects.filter(email=email1)
        if users.count() == 0:
            raise forms.ValidationError(_('Δεν υπάρχει χρήστης με αυτό το e-mail'))


class PasswordForm(forms.Form):
    password1 = forms.CharField(label=_('Νέος κωδικός πρόσβασης'), max_length=100,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(label=_('Νέος κωδικός πρόσβασης (επανάληψη)'), max_length=100,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        validate_password(password1, password2)
