from dal import autocomplete
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core.forms import GenericModelForm
from .checks import validate_password
from .models import StaffMember


class StaffForm(GenericModelForm):
    scoped_fields = ['internal_department']

    class Meta:
        fields = ['email', 'given_name', 'surname', 'institution', 'school',
                  'department', 'title', 'is_internal', 'internal_department',
                  'can_apply_for_phd', 'can_review_phd_apps', 'can_post_theses']
        model = StaffMember
        labels = {
            'email': _('Ε-mail'),
            'given_name': _('Όνομα'),
            'surname': _('Επώνυμο'),
            'institution': _('Ίδρυμα'),
            'school': _('Σχολή'),
            'department': _('Τμήμα'),
            'internal_department' : _('Τμήμα εντός του ιδρύματος'),
            'title': _('Ιδιότητα'),
            'is_internal': _('Είναι εσωτερικός;'),
            'can_apply_for_phd' : _('Μπορεί να κάνει αίτηση για διδακτορικό'),
            'can_review_phd_apps' : _('Μπορεί να είναι αξιολογητής σε αιτήσεις διδακτορικού;'),
            'can_post_theses' : _('Μπορεί να είναι επιβλέπων ή μέλος επιτροπής διπλωματικών;')
        }
        widgets = {'internal_department': autocomplete.ModelSelect2(
            url='curricula:department-autocomplete',
            attrs={
                'data-theme': 'bootstrap-5',
                'data-allow-clear': 'false',
                'class': 'bootstrap5-autocomplete',
                'data-placeholder': _('Επιλέξτε εσωτερικό τμήμα')}
        )}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     is_internal = self.data.get('is_internal')
    #
    #     if is_internal is None:
    #         is_internal = self.initial.get('is_internal')
    #
    #     if not is_internal:
    #         self.fields['internal_department'].widget = forms.HiddenInput()



class SignUpForm(forms.Form):

    email = forms.EmailField(label=_('Το email σας') )
    name = forms.CharField(label=_('To μικρό σας όνομα'), max_length = 40)
    surname = forms.CharField(label=_('To επίθετο σας'),max_length = 100)
    password1 = forms.CharField(label=_('Κωδικός πρόσβασης'),max_length = 100, widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(label=_('Κωδικός πρόσβασης (επανάληψη)'),max_length = 100, widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

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
            raise forms.ValidationError( _('Δεν μπορείτε να χρησιμοποιήσετε διεύθυνση ταχυδρομείου @') + settings.INTERNAL_DOMAIN)

        User = get_user_model()
        users = User.objects.filter(email = email)
        if users.count() > 0:
            raise forms.ValidationError(_('Υπάρχει ήδη χρήστης με αυτό το e-mail') )
        
        return cleaned_data
        
class RegisterForm(forms.Form):

    email1 = forms.EmailField(label=_('Το e-mail σας:') )
    email2 = forms.EmailField(label=_('Το e-mail σας (ξανά):') )
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean(self):
        cleaned_data = super().clean()
        if ('email1' not in cleaned_data) or ('email2' not in cleaned_data):
            raise forms.ValidationError( _('Εισάγετε μία έγκυρη διεύθυνση ηλεκτρονικού ταχυδρομείου') )
        
        email1 = cleaned_data['email1']
        email2 = cleaned_data['email2']
        
        if email1 != email2:
            raise forms.ValidationError(_('Τα email πρέπει να ταυτίζονται!') )
        
        if settings.INTERNAL_DOMAIN in email1:
            raise forms.ValidationError( _('Αν έχετε ήδη email της μορφής @') + settings.INTERNAL_DOMAIN + _(' δεν χρειάζεται να εγγραφείτε.') )
        
        User = get_user_model()
        users = User.objects.filter(email = email1)
        if users.count() > 0:
            raise forms.ValidationError( _('Υπάρχει ήδη χρήστης με αυτό το e-mail') )

class ForgotPasswordForm(forms.Form):
    email1 = forms.EmailField(label= _('Το e-mail σας:'))
    email2 = forms.EmailField(label= _('Το e-mail σας (ξανά):'))
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean(self):
        cleaned_data = super().clean()
        if ('email1' not in cleaned_data) or ('email2' not in cleaned_data):
            raise forms.ValidationError(_('Εισάγετε μία έγκυρη διεύθυνση ηλεκτρονικού ταχυδρομείου'))
        
        email1 = cleaned_data['email1']
        email2 = cleaned_data['email2']
        
        if email1 != email2:
            raise forms.ValidationError(_('Τα email πρέπει να ταυτίζονται!'))
        
        if settings.INTERNAL_DOMAIN in email1:
            raise forms.ValidationError(_('Αν έχετε ήδη email της μορφής @') + settings.INTERNAL_DOMAIN + _(' δεν μπορείτε να επαναφέρετε τον κωδικό σας μέσω αυτού του συστήματος.') )
        
        User = get_user_model()
        users = User.objects.filter(email = email1)
        if users.count() == 0:
            raise forms.ValidationError(_('Δεν υπάρχει χρήστης με αυτό το e-mail') )
        
          
class PasswordForm(forms.Form):

    password1 = forms.CharField(label=_('Νέος κωδικός πρόσβασης'),max_length = 100, widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(label=_('Νέος κωδικός πρόσβασης (επανάληψη)'),max_length = 100, widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        validate_password(password1, password2)

